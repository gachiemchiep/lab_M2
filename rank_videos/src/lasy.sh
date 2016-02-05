#!/usr/bin/env bash


if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

# Extract feature
bash extract_features.sh test.cfg



bash ../src/VisualRank.sh UCF-101_imgs.conf
bash merge_features.sh test.cfg
# Calculate distance
bash cal_dists.sh test.cfg
bash merge_dists.sh test.cfg

# result will be test_vids_fc7_dists.mat
# after that use this to rank video