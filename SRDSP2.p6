#!/usr/bin/perl6
#
use JSON::Tiny;
# my $s = 'нӓқэлешпугу /об. Ч, вас., тым./ отгл. гл., пер./непер., конкрпроц., НС - 1) тянуть; 2) натягивать; 3) курить; см. нӓқлешпугу'
# my $s = 'нӓдэ́бэ́гу /об. С/ отгл. гл., непер., пас., НС - быть женатым; см. нӓдэббэ́гу'
# my $s = 'нӓдэ́бэ́л /тым./ прич. от гл. нӓдэ́бэ́гу; см. калдап';
 my $s = 'нӓлдёлгу /об. Ш/ гл., пер., однокр., С- 1) затоптать: таб нежбо нӓлдённыт /об. Ш/ «он наступил (букв. затоптал) на шиповник»; см. нӓльдёлгу; няльдёлгу';
# my $s = 'нӓқыттықо /тур./ отгл. гл., непер., характ., НС - курить обычно: тэп мелко кансазэ нӓқытта «он всегда трубку (букв. трубкой)курит»';
#my $s = 'тймбэ́ккугу ~ тймбэ́кугу /кет./ отгл. гл., непер., повт., НС - летать систематически: қамбан нюрбаррн тймбэ́кваттэ́ ламбреккала «весной над лугом летают бабочки»';
# my $s = 'нӓл ~ нӓль /об. Ш, вас., тым./ сущ. нӓ, ф. опред. - женский';
# my $s = 'явол /тур./ сущ. - 1) дьявол; 2) чёрт (< русск.): яволыт қыйты! «чёртов дух!»';
# my $s = 'я /об. Ч/ отриц. част. - не: ~ шыдедуқут «не врём»; ӣл най шындэ ~ қостэла «сын-твой опять тебя не узнает»; см. а'
# my $s = 'эҗ ~ эҗэ /об., кет., вас., тым./ ~ эҗо ~ эҗи /кет./ сущ. - 1) голос: қун эҗап ӧнтэльдяп /об. Ш/ «голос человека услышал-я»; қун эҗэм ӱндыдисав /кет./ «голос человека услышал-я»; табэ қыгыс парқугу, эҗэдэ нету];а /об. Ч/ «он хотел кричать, голоса-его не было»; окэр челҗоқот пыкан аңмут эҗэ чаннэнҗа /об. Ч/ «однажды изо рта быка голос вышел» (из ск.); 2) слово: онэндэ эҗэм оралбэгу /кет./ «своё слово сдержать»; қудэ ташшэндэ огхолалҗешпа қоштэл эҗэп чэнчугу? /об. Ч/ «кто тебя учит плохое слово говорить?»; 3) язык (речь): қулэй эҗэ /кет./ «человеческий язык»; қульдиң нимдйкваттэ тэ эҗан? /кет./ «как называется на вашем языке?»; 4) речь: ме ӱндыдет тэбын эҗэм соң /кет./ «мы слушали его речь внимательно»; 5) разговор; 6) легенда; 7) сказание; 8) предание: таб эҗэлгук: “Қаиль на эҗ? Ман ныльҗи эҗэ тӓнундак, шэнҗэ а кадэшпал” /об. Ч/ «она говорит: “Разве это предание? Я такое предание знаю, (что) языком не расскажешь”»; см. эҗ';
# my $s = 'атымбыгу /об. Ч/ нареч., м.-вр. п. - наверху: хэр ~ коимба «снег наверху кружится»';
#my $s = 'атымбыгу /об. Ч/ сущ. - появиться: хэр ~ коимба «снег наверху кружится»';
#my $s = 'аттэкочэ́гу /тым./ отгл. гл., непер., возвр., НС - прятаться';
#my $s = 'атымбыгу /кет./ отгл. гл., непер., результ. сост. ~ пас., С/НС - 1) появиться, заблудиться (да): хэр ~ коимба «снег наверху кружится»';
# my $s = 'қолҗэл /об. Ч, тым./ ~ қольҗэль /тым./ 1. прил. - 1) кривой; 2) косой; 2. сост. ч. имен. сказ.: ман ильманнан хайдэ қольҗэң эя /тым./ «мой ребёнок косоглазый (букв. у моего ребёнка глаз-его косой)» қолҗэль';
#my $s = 'қольчиқо / тур./ гл., пер., инт.-перф., С - увидеть; см. қольдигу';
#my $s = 'қудя /кет./ сущ. - щенок: тюмбэнэ пӱдуң қудяны «волчонок похож на щенка»; қудяққа ~ қудюққа уменьш.';
#my $s = 'ти́тяткынны /кет./ нареч., исх. п. - отсюда: қаиңго тан ~ қвэ́ссандэ́? «почему ты отсюда ушёл?»';
# my $s = 'шӧк /тым/ сущ. - 1) самка; 2) кобыла; см. шӧв';
# my $s = 'иметий /ел./ отым. прил. - женский: ~ қаймпоргх; «женское платье»';
grammar article {
	rule TOP {
		<title_wrap> <meaning_wrap>? ";"?
	}
	token title_wrap {
		<title_pair>+ % [ [ \h* \~ \h* ] * ] \h* <prop_wrap>?
	}
	token title_pair {
		<title> <geo_marking>? \h* <prop_wrap>? \h*
	}
	token title {
		<symbol_strict>+ % [ \h* ]
	}
	# symbol abstracts
	token symbol_strict {
		<alpha>
	}
	token symbol_med {
		[
			|| <alpha>
			|| <?after <alpha>> [ <digit> || <punct> ] + <?before <alpha>>
			|| "-"
		]
	}
	# see group
	token see_group {
		\; \h* "см" "."* \h* <see>+ % [ [ [ ";" || ","] \h* ] * ]
	}
	token see {
		<symbol_med>+ % [ \h * ]
	}
	# meaning
	token meaning_wrap {
		\h*
		[
			|| "-"* \h* <par_numbered_ma>
			|| "-"* \h* <simple_ma>
			|| <point_numbered_ma>
		]
	}
	token meaning {
		[ <symbol_med> || "(" || ")" || "."  || "<" || "?" || < [ “ ” ] > ] + % [ \h * ]
	}
	# examples
	token examples {
		":" \h + <example_group>
	}
	token example_group {
		<example> + % [ [ \;\s+ ] ? ]
	}
	token example {
		<original>
		<geo_marking>* [\h || \;]*
		[ "«" <translation> "»" ] *
		<comment_wrap>*
	}
	token comment_wrap {
		\s+ \( <comment> \)
	}
	token comment {
		<-[ \( \) ]>*
	}
	token original {
		[ <symbol_med> || <:punct - [«»\/\;]> || "~" ] + % [ \h* ]
	}
	token translation {
		<-[«»]> +
	}
	# # point numbered meaning arr
	token point_numbered_ma {
		<po_meaning_group>+ % [ "; " * ]
	}
	token po_meaning_group {
		\d+ "." \h* <meaning>+ % [ [ \h* [";" || ","] \h* ] * ] <examples>*
	}
	# # parenthesis numbered meaning arr
	token par_numbered_ma {
		<pm_meaning_group>+ % [ "; " * ]
	}
	token pm_meaning_group {
		\d+ ")" \h* <meaning>+ % [ [ \h* [";" || ","] \h* ] * ] <examples>*
	}
	# # simple meaning arr
	token simple_ma {
		<si_meaning_group>+ % ["; " * ]
	}
	token si_meaning_group {
		<meaning>+ % [ [  \h* [";" || ","] \h* ] * ] <examples>*
	}
	# properties
	token prop_wrap {
		<property> + % [ [ \h*\,\h* || \h*\~\h* ] ? ]
		<external_property>?	
	}
	token property {
		[
			|| [ <alpha>\.* ] + % [ [ \s+ || "/" || "-" ] ? ]
			|| [ <[А..Я]> ] + % [ "/" ? ]
		]
	}
	token external_property {
		[
			\h* "-"
			[  \h* \w+ % [ \h* ] \?  ] +
		]
	}
	# geo marking
	token geo_marking {
		\h+ "/" \h* <geo_marks> \h* "/"
	}
	token geo_marks {
		<geo_mark>+ % [ ", "* ]
	}
	token geo_mark {
		[ <geo_obsk> || <geo_default> ]
	}
	token geo_obsk {
		"об" [ \. || \h ] *
		["С" || "Ч" || "Ш" || "III"]+ % [ ", "* ]
		\.*
	}
	token geo_default {
		\w+ \.*
	}
};

# IO declarations
my $str = open 'srds-splitted-final.txt';
my $output = open 'srds-parsed.json', :a;
# 

my @data = $str.lines();

grammar check_for_see {
	rule TOP {
		.+ <see_group>
	}
	token symbol_med {
		[
			|| <alpha>
			|| <?after <alpha>> [ <digit> || <punct> ] + <?before <alpha>>
			|| "-"
		]
	}
	# see group
	token see_group {
		\; \h* "см" "."* \h* <see>+ % [ [ [ ";" || ","] \h* ] * ]
	}
	token see {
		<symbol_med>+ % [ \h * ]
	}
}
my $add = '';
my $i = 0;
### OVER |
for @data -> $final is copy {
	$final = $final.trim;
	if ( $add ne '' ) {
		$final ~= $add;
		$add = '';
	}
	my $see_check = check_for_see.parse($final);
	my @see_occs = $see_check ?? $see_check<see_group><see>.map(*.Str) !! [];
	$final ~~ s:g/\; \h* "см" \.* \h+ .* $//;
	my $parsed = article.parse($final);
	if ( ! $parsed ) {
		$final ~~ /<-[\h\s]>+ $/ and my $add = $/.Str ~ ' ';
		$final ~~ s:g/\h* <-[\h\s]>+ $//;
		$parsed = article.parse($final);
		if ( ! $parsed ) {
			$add = '';
			next;
		}
	}
	my %format = "title" => [], "lexic" => [], "see" => @see_occs;
	for $parsed<title_wrap><title_pair> {
		my %cur_hash;
		%cur_hash<query> = $_<title>.Str;
		%cur_hash<dialects> = [];
		if ( $_<geo_marking> ) {
			%cur_hash<dialects> = $_<geo_marking><geo_marks><geo_mark>.map(*.Str);
		}
		if ( $_<prop_wrap> ) {
			%cur_hash<props> = $_<prop_wrap><property>.map(*.Str);
		}
		%format<title>.push: %cur_hash;
	}
	my $holder = '';
	my $subcat = '';
	given $parsed<meaning_wrap> {
		when $_<par_numbered_ma> {
			$holder = 'par_numbered_ma';
			$subcat = 'pm_meaning_group';
		}
		when $_<simple_ma> {
			$holder = 'simple_ma';
			$subcat = 'si_meaning_group';
		}
		when $_<point_numbered_ma> {
			$holder = 'point_numbered_ma';
			$subcat = 'po_meaning_group';
		}
	}
	%format<lexic> = [];
	for $parsed<meaning_wrap>{$holder}{$subcat} {
		my @meaning = $_<meaning>.map(*.Str);
		my @examples = [];
		for $_<examples>[0]<example_group><example> -> $e {
			my $example = $e;
			my %example_hash;
			%example_hash<selkup> = $example<original>.Str;
			if ( $example<geo_marking> ) {
				%example_hash<dialects> = $example<geo_marking>[0]<geo_marks><geo_mark>.map(*.Str);
			}
			if ( $example<translation> ) {
				%example_hash<russian> = $example<translation>.Str;
			}
			@examples.push: %example_hash;
		}
		my %ins_hash;
		%ins_hash<meaning> = @meaning;
		if ( @examples != [] ) {
			%ins_hash<examples> = @examples;
		}
		%format<lexic>.push: %ins_hash;
	}
	$output.say(to-json(%format) ~ ",");
	say $i;
	++ $i;
}
$output.close();
