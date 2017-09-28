#!/usr/bin/perl6
grammar testing {
	rule TOP {
		<multi> **? 1 .+? <multi> **? 1 .+
	}
	token multi {
		<title_wrap>+?
	}
	token title_wrap {
		<title_pair>+ % [ [ \h* \~ \h* ] * ] \h* <prop_wrap>+
	}
	token title_pair {
		<title> <geo_marking>+
	}
	token title {
		<alpha>+ % [ \h* ]
	}
	# properties
	token prop_wrap {
		<property> + % [ [ \h*\,\h* || \h*\~\h* ] ? ]
	}
	token property {
		[
			|| [ <alpha>\.* ] + % [ [ \s+ || "/" || "-" ] ? ]
			|| [ <[А..Я]> ] + % [ "/" ? ]
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
grammar spl {
	rule TOP {
		<title> <common>
	}
	token title {
		<alpha>+ % [ \h* ]
	}
	token common {
		<-alpha - [\h]> .+
	}
};
my $in = open 'srds-splitted.txt';
my $out = open 'srds-splitted-final.txt', :a;
#my $fh = 'араннэ́л /об. Ч/ отым. прил. - осенний аранпӓр /об. С/ сущ. - сарай';
my @la = [];
my $i = 0;
for $in.lines() -> $line is copy {
	$line = $line.trim;
	if ( testing.subparse($line) ) {
		my $second_dirty = testing.subparse($line)<multi>.map(*.Str)[1];
		my $sp = spl.subparse($second_dirty);
		my $title = $sp<title>.Str;
		my $common = $sp<common>.Str;
		my $second_modified = split(/\h+/, $title, 2).join("\n") ~ " " ~ $common;
		$line ~~ s/$second_dirty/{$second_modified}/;
	}
	$out.say($line);
	say($i);
	++ $i;
}
$out.close;
