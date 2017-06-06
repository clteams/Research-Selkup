#!/usr/bin/perl6
my $srds_bit = 'srds-ex.txt'.IO.slurp;
#say $srds_bit;
grammar main_gram {
	rule TOP {
		<section>* % ["\n"+]
	}
	token section {
		<title_wrap> <stopping>
	}
	#тэйези ~ тэйезой /об С, кет./ прил. облад. - умный: тап адуң тэйези /об. С/ «он, кажется, умный»
	token title_wrap {
		<title> <sub_title>*
	}
	token title {
		# todo: all native word symbols from SRDS (and include \s)
		<-[\/\-\.~,:\(\)\d]>*
	}
	token sub_title {
		" ~ " <title>
	}
	token stopping {
		<-[\n\t]>*
	}
};
say main_gram.parse($srds_bit);
