#!/usr/bin/perl6
#
use JSON::Tiny;
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
