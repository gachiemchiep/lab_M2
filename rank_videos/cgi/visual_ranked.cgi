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
    my $action = $q->param('action') || $default_action;

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
        -title => 'Display Visual Rank result',
        -bgcolor => 'white',
        -style => {'src' => './style/index.css'},
    );
    print $q->h2("Display Visual Rank result");
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

    # 3 of these results should be displayed as the same time
    # in the same table
    # from left to right : 10opflows, imgs, ST

    my @verb_indexes = ();
    for (my $verb_index = 0; $verb_index < 101; $verb_index = ($verb_index + 1)) {
        push(@verb_indexes, $verb_index);
    }

    my @result_files = ("VisualRank/UCF-101_vids_fc7_10opflows.txt",
    "VisualRank/UCF-101_vids_fc7_imgs.txt",
    "VisualRank/UCF-101_vids_fc7_ST.txt",
    "VisualRank/UCF-101_vids_fc7_10opflows_siamese.txt",
    "VisualRank/UCF-101_vids_fc7_imgs_siamese.txt",
    "VisualRank/UCF-101_vids_fc7_ST_siamese.txt");

    print $q->start_form(
        -name => 'action',
        -method => 'POST',
    );
    print $q->start_table();
    print $q->Tr(
        $q->td(
            $q->p('Select result files'),
            $q->checkbox_group(
                -name     => 'result_files',
                -values   => \@result_files,
                -defaults => [$result_files[1], $result_files[2]],
                -columns  => 1,
                -rows     => $#result_files,
            ),
        ),
        $q->td(
            $q->p('Select verb index'),
            $q->popup_menu(
                -name => 'verb_index',
                -values => \@verb_indexes,
                -default => "$verb_indexes[2]",
            ),
        ),
        $q->td(
            $q->submit(
                -name => 'action',
                -value => 'show_results',
            )
        ),
        $q->td('&nbsp;'),
    );

    print $q->end_table();
    print $q->end_form();
}

#get the comtain
sub get_lines {

    my ($q, $file, $index) = (@_);
    print $q->p("$file");
    open(DATA, "<$file") or die $q->p("$file Not found");

    my @markers;
    my @lines_tmp;
    my $line_count = 0;

    while(<DATA>) {
        my $line = $_;
        $line =~ s/"\n"//g;
        push(@lines_tmp, $line);

        if (index($line, "###") != - 1) {
            push(@markers, $line_count);
        }
        $line_count = $line_count + 1;
    }
    close(DATA);

    my $marker_start = $markers[$index];
    my $marker_end = $markers[$index + 1];

    my @selected_lines = @lines_tmp[($marker_start + 1) .. ($marker_end - 1)];

    return @selected_lines;

}

#print the image
sub print_img {
    my ($q, $vid_file) = (@_);

    my $vid_path = "/export/data/corel/UCF-101/";
    my $vid_path_new = "./VIDS/";
    my $thm_path = "./THMS/";
    my $thm_ext = "_1.jpg";

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
    );
}

# show ranking results
sub show_results {

    my ($q) = @_;

    # select verb index
    my $verb_index = $q->param('verb_index');
    my @result_files = sort $q->param('result_files');

    my @lines;
    my $files_count = scalar @result_files;
    my $lines_count;

    for (my $count = 0; $count <= $#result_files; $count++) {
        my @file_lines = get_lines($q, $result_files[$count], $verb_index);
        for (my $col = 0; $col < $#file_lines; $col++) {
            $lines[$count][$col] = $file_lines[$col];
        }
        $lines_count = scalar @file_lines;
    }

    #print $q->p("@$_"), "\n" foreach ( @lines );

    print $q->p("aaaaa");

    print $q->p("$lines_count");
    my $row_count = int($lines_count / 3);

    print $q->p("$files_count");
    print $q->p("$row_count");

    for (my $row = 0; $row <= $row_count; $row++) {

        print $q->start_table(
            {-border => 3},
        );
        print $q->start_Tr();

        for (my $count = 0; $count < $files_count; $count++) {

            my $col_start = $row * 3;
            my $col_end = ($row + 1) * 3;

            for (my $col = $col_start; $col < $col_end; $col++) {
                print_img($q, $lines[$count][$col]);
            }
            print $q->td(
                $q->a(
                    {href => "nothing"},
                    $q->img(
                        {-src => "",
                        -height => 80,
                        -width => 80 }
                    )
                ),
            );

        }

        print $q->end_Tr();
        print $q->end_table();
    }

}
