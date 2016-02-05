#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

printf "$VIDS_LIST \n";
printf "$OPFLOWS_LIST \n";
printf "$SRC_DIR \n";

# merge into biggest
name=$( basename ${VIDS_LIST});
find ${DIST_DIR} -type f -name "${name%.*}_${LAYER}_*.mat" | sort > dists_list.txt;
name=$( basename ${VIDS_LIST});

/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');merge_dists('$VIDS_LIST','$OPFLOWS_LIST','$PWD/dists_list.txt','$PWD/${name%.*}_${LAYER}_dists.mat'); quit";

rm $PWD/${name%.*}_${LAYER}_ranked.txt;
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');rank_dists('$PWD/${name%.*}_${LAYER}_dists.mat',$TOP_COUNT,'$PWD/${name%.*}_${LAYER}_ranked.txt'); quit";