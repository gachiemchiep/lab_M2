#!/usr/bin/perl
#Note , change $display_results if needed
use strict;
use warnings FATAL => 'all';
use CGI;
use CGI::Carp qw(fatalsToBrowser); # Remove this in production
use File::Basename;

my $q = new CGI;

# Dispatch table for handling action
my %allowed_actions = (
        # default action
        show_form => \&show_form,
        # main form action
        show_results => \&show_results,
);

print $q->header();

# Output stylesheet, heading etc
print_head($q);

handle_form($q);

# Output footer and end html
print_tail($q);

exit 0;

#-------------------------------------------------------------

# Handle form
sub handle_form {
    my ($q) = @_;
    my $default_action = 'show_form';
    my $action =$q->param('action') || $default_action;

    print $q->p("select: ".$action);
    # Sanity check
    if (not exists $allowed_actions{$action}) {
        print $q->p("Unknown action: ".$action."Forcing to ".$default_action." instead.");
        $action = $default_action;
    };
    my $code = $allowed_actions{$action};

    # Now call the code
    $code->($q);
}

# Outputs the start html tag, stylesheet and heading
sub print_head {
    my ($q) = @_;
    print $q->start_html(
        -title => 'Display ranked videos using Euclid distances',
        -bgcolor => 'white',
        -style => {'src'=>'./style/index.css'},
    );
    print $q->h2("Display ranked videos using Euclid distances");
}

# Outputs a footer line and end html tags
sub print_tail {
    my ($q) = @_;
    # print the return button here
    print $q->end_html;
}

# main submit form
sub show_form {
    my ($q) = @_;

    my @result_files = ("UCF-101_p1_vids_fc7_ranked.txt", "UCF-101_p1_vids_fc7_ranked_dis.txt");
    my @list_indexes = ();
    for (my $list_index=0; $list_index <= 3873; $list_index=($list_index+100)) {
        push(@list_indexes, $list_index);
    }
    my @rank_indexes = ();
    for (my $rank_index=1; $rank_index <= 300; $rank_index=($rank_index+10)) {
        push(@rank_indexes, $rank_index);
    }

    print $q->start_form(
        -name =>'action',
        -method => 'POST',
    );
    print $q->start_table();
    print $q->Tr(
            $q->td(
                $q->p('Select result file'),
                $q->popup_menu(
                        -name => 'result_file',
                        -values => \@result_files,
                        -default => "$result_files[1]",
                ),
                $q->p('Select list index'),
                $q->popup_menu(
                    -name => 'list_index',
                    -values => \@list_indexes,
                    -default => "$list_indexes[2]",
                ),
                $q->p('select rank start index'),
                $q->popup_menu(
                    -name => 'rank_index',
                    -values => \@rank_indexes,
                    -default => "$rank_indexes[2]",

                ),
            ),
            $q->td($q->submit(
                -name => 'action',
                -value => 'show_results',
            )),
        $q->td('&nbsp;'),
        );

    print $q->end_table();
    print $q->end_form();
}

# show ranking results
sub show_results {

    my $vid_path = "/export/data/corel/UCF-101/";
    my $vid_path_new = "./VIDS/";
    my $thm_path ="./THMS/";
    my $thm_ext = "_1.jpg";

    my ($q) = @_;
    my $result_file = $q->param('result_file');
    # Read result file from list_index th line
    my $list_index = $q->param('list_index');
    # which part of list
    my $rank_index = $q->param('rank_index');

    open(DATA,"<$result_file") or die $q->p("$result_file Not found");

    my $list_end = $list_index + 100;

    print $q->p("$list_index");
    print $q->p("$list_end");

    my $line_count = 0;
    my @lines;
    while(<DATA>) {
        $line_count = $line_count + 1;
        if (($line_count > $list_index) && ($line_count < $list_end)) {
            my $line = $_;
            $line =~ s/"\n"//g;
            push(@lines, $line);
        }
    }
    close(DATA);

    if ($#lines == 0) {
        $q->p("Selected index $list_index is too big");
        $q->p("Selected index smaller than $line_count");
    } else {
#        for (my $row=0; $row <= $#lines; $row++) {
#            print $q->p("$lines[$row]");
#        }
        # print result
        for (my $row=0; $row <= $#lines; $row++) {
            my $line = $lines[$row];

            print $q->start_table(
                {-border => 3},
            );
            print $q->start_Tr();

            my @line_pairs_all = split(',', $line);
            my @line_pairs = ();
            push(@line_pairs, $line_pairs_all[0]);
            push(@line_pairs, @line_pairs_all[$rank_index..($rank_index+10)]);

            for (my $col=0; $col <= $#line_pairs; $col++) {

                my $pair = $line_pairs[$col];
                my @pair_split = split(/:/, $pair);

                my $vid_file = $pair_split[0];
                my $dist = $pair_split[1];

#                my $vid_file = $line_files[$col];
                (my $vid_file_new = $vid_file) =~ s/$vid_path/$vid_path_new/;
                (my $thm_file = $vid_file) =~ s/$vid_path/$thm_path/;
                $thm_file =~ s/\.avi/$thm_ext/;
                my $basename = basename($vid_file);

                print $q->td(
                    $q->a(
                        {href => "$vid_file_new"},
                        $q->img(
                            {-src => "$thm_file",
                            -height => 80,
                            -width => 80 }
                        )
                    ),
                    $q->p("$basename"),
                    $q->p("$dist"),
                );
            }

            print $q->end_Tr();
            print $q->end_table();

        }

    }
}


