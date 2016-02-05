#!/usr/bin/perl
use strict;
use warnings FATAL => 'all';

my @nums = (1..20);
print "@nums";

for (my $index=0; $index <= 13320; $index=($index+50)) {
    print "$index \n"
}