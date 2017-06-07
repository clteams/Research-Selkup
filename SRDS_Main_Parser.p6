#!/usr/bin/perl6

###my $srds_bit = 'srds-ex.txt'.IO.slurp;

grammar word_start {
	rule TOP {
		[ <title_group> \s* <geo_marking> ] + % [\s*] <properties>* <meaning_wrap>
	}
	token title_group {
		[" ~ " || "~ "] * <title>+ % ["~ "*]
	}
	token title {
		<-[\/~,]>+
	}
	token properties {
		<property>+ % [", "+]
	}
	token property {
		[ [ \w+\. ] + % [" "+] || <[А..Я]> ]
	}
	token geo_marking {
		"/" <geo_marks> "/"
	}
	token geo_marks {
		<geo_mark>+ % [", "*]
	}
	token geo_mark {
		[ <geo_obsk> || <geo_default> ]
	}
	token geo_obsk {
		"об. " ["С" || "Ч" || "Ш"]+ % [", "*] \.*
	}
	token geo_default {
		\w+ \.
	}
	token meaning_wrap {
		"-" \s* <numbered_mgroup>
	}
	# common meaning related tokens
	token w_selkup {
		# todo: "\w+" -> selkup alphabet list
		\w+
	}
	token wm_selkup {
		<w_selkup>+ % [\s+]
	}
	token meaning {
		# todo: maybe change smth
		<wm_selkup>
	}
	token example_wrap {
		# maybe ": " -> ":\s*"
		": " <example>+
	}
	token example {
		<wm_selkup> \s* <geo_marking>* \s* <explanation_wrap>
	}
	token explanation_wrap {
		# todo: check if there are some other types of bracketing
		«<explanation>»
	}
	token explanation {
		# todo derived from the previous token
		<-[«»]>+
	}
	# numbered meaning group
	token numbered_mgroup {
		\d+\) <numbered_mgroup_part> <?before \d>
	}
	token numbered_mgroup_part {
		<meaning> <nmp_example_wrap>*
	}
	token nmp_example_wrap {
		": " <example>+ % ['; '+]
	}
	# <<-[,]>+>* %[', '*]
};
#my $test_str = "~ агылдэ́гу ~ слово /тым./ ~ овсло /об. С/";
# немного поесть ! авыт ...
# #my $test_str = "авырэ́гу /кет./ отгл. гл., пер., смягч., С - немного поесть авыт /об. Ш/ указ. местм. - другой";

my $test_str = 'абсод ~ абсбдй /об. С/ сущ. - 1) пища, еда: могай абсод /об. С/ «мучная пища»; абсодй нюэтй /об. С/ «еда вкусная»; 2';


say word_start.subparse($test_str);
#say $test_str ~~ /(<-[\/~]>+)+ % ["~ "*]/;

#say $srds_bit;
#абыл кай /об. Ч/ сост. наим. - уха
#авырэ́гу /кет./ отгл. гл., пер., смягч., С - немного поесть авыт /об. Ш/ указ. местм. - другой: мат қванэшпак пот паровыт ~ пэлэккай ӧттомн «я иду по лесине на другой берег реки» авэлҗэ́гу /вас./ гл., пер., С - забыть: ӣҗэ, қоромҗэ қонэ^ыт ӓвэлҗап /вас./ «Иҗэ, лукошко наверху забыла-я»; см. аволҗэ́гу авэшпугу /об. Ш/ отгл. гл., пер., конкр.-проц., НС - 1) есть, ку- шать: авэ́шпэт, пади нӯнҗанд /тьм./ «ешь, поди устал-ты»; ми авэ́шпызыт қвэ́лып /об. Ш/ «мы ели рыбу»; 2) кусать (о насекомых): табып ныңкала авэ́шпӓт /об. Ш/ «его комары кусают»; см. авешпугу авэ́ /кет./ сущ. - 1) мать; 2) тётя; см. ава I
#авэ́ргу /об.Ч., кет/ отгл. гл., пер., НС - есть, кушать; см. авыргу авэ́ргунҗялк /об. Ч/ нареч. необл. - 1) голодом; 2) натощак: қайм мат тека нагэ́рбам, нагур бар чел ~ «что я вам пропи- шу, три раза в день натощак (принимать)» авэ́ргун пара /об. Ч/ словосоч. - обеденное время авэ́ртэ /об. Ш/ имя действ. 1 от гл. авыргу - еда; см. авыртэ ага /кет./ ~ агӓ /об. С, Ш/ ~ ака /тым./ сущ. - 1) брат: нэпт агат /об. Ш/ «имя брата»; агау нэтэҗиң /об. С/ «брат-мой женит- ся»; варр ~ /об.С/ «старший брат»; 2) старший брат агораҗгу /тым./ гл., пер., С - загородить (< русск.) агылгу /вас./ гл., непер., НС - лениться
#агылдэ́гу /тым./ ~ агылҗугу /об. Ч/ гл., пер., С - обидеть: таб а кыга тажэ́нды агылҗугу кек /об. Ч/ «он не хочет тебя сильно обидеть»

