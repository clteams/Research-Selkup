#!/usr/bin/perl6

###my $srds_bit = 'srds-ex.txt'.IO.slurp;

# not only word_start should be there
#

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
		[
			[ \w+\. ]+ % [ " "+ ]
			|| <[А..Я]>
		]
	}
	token geo_marking {
		"/" <geo_marks> "/"
	}
	token geo_marks {
		<geo_mark>+ % [ ", "* ]
	}
	token geo_mark {
		[ <geo_obsk> || <geo_default> ]
	}
	token geo_obsk {
		"об. "
		["С" || "Ч" || "Ш"]+ % [ ", "* ]
		\.*
	}
	token geo_default {
		\w+ \.
	}
	token meaning_wrap {
		# todo: add different meaning formats, not only numbered_mgroup
		\s* \- \s*
		\d+ \) \s*
		<numbered_mgroup>+ % [
			[
				\; \s* \d+ \) \s*
			] +
		]
	}
	# common meaning related tokens
	token w_selkup {
		# todo: "\w+" -> selkup alphabet list
		\w+
	}
	token wm_selkup {
		\w+ % [ \s+ ]
	}
	token meaning_group {
		# todo: maybe change smth
		<meaning>+ % [ ", "* ]
	}
	token meaning {
		<[А..ЯЁа..яё]>+
	}
	token example_wrap {
		# maybe ": " -> ":\s*"
		": " <example>+
	}
	token example {
		<original>+ \s*
		<geo_marking>* \s*
		<explanation_wrap>
	}
	token original {
		#todo: \w+ -> link to wm_selkup
		[ \w || "~" ]+ % [ \s* ]
	}
	token explanation_wrap {
		# todo: check if there are some other types of bracketing
		"«" <explanation> "»"
	}
	token explanation {
		# todo derived from the previous token
		<-[ «  » ]>+
	}
	# numbered meaning group
	token numbered_mgroup {
		<numbered_mgroup_part>
	}
	token numbered_mgroup_part {
		\s* <meaning_group> \s* <nmp_example_wrap>*
	}
	token nmp_example_wrap {
		": "
		<example>+ % [ '; '+ ]
	}
};
my $test_str = 'абсод ~ абсбдй /об. С/ сущ. - 1) пища, еда: могай абсод /об. С/ «мучная пища»; абсодй нюэтй /об. С/ «еда вкусная»; 2) семена: пақэ́лпэ́дй чочэм абсодэсэ омдэ́лҗыгу керегең /об. С/ «паханую землю семенами засеять надо»;';

say word_start.subparse($test_str);

