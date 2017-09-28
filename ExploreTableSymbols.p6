#!/usr/bin/perl6
use v6;
use DBIish;
use JSON::Tiny;
# explore the dictionary database
my $dictionary = DBIish.connect("SQLite", :database<dic.sqlite3>);
my $req = $dictionary.prepare(q:to/STATEMENT/);
	select title, content from srds_dictionary
STATEMENT
$req.execute();
my @got = $req.allrows();
my @symbols = [];
my $index = 0;
for @got -> @case {
	my $title = @case[0];
	my $content = from-json(@case[1]).Str;
	my @syms = $title ~~ m:g/<-[А..ЯЁа..яё\h\s]>/;
	@syms.append: $content ~~ m:g/<-[А..ЯЁа..яё\h\s]>/;
	for @syms -> $sym {
		if $sym ne any(@symbols) {
			@symbols.push: $sym;
		}
	}
	"index $index".say;
	++ $index;
}
@symbols.join(' ').say;
#
