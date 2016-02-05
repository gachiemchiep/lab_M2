#!/usr/bin/env bash


#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

printf "$VIDS_LIST \n";
printf "$OPFLOWS_LIST \n";
printf "$FEATURE_DIR \n";
printf "$SRC_DIR \n";

CMDS_FILE=$PWD/VisualRank.txt
rm $CMDS_FILE;

verb_mats=$( find $VERBS_FEATURE_DIR -type f -name "*.mat" -not -name "*_ranked.mat" );

if [ ! -d $VERBS_FEATURE_RANKED_DIR ]; then
  mkdir $VERBS_FEATURE_RANKED_DIR;
fi

for verb_mat in ${verb_mats[@]}; do

  verb_mat_rank=$( printf "$verb_mat" | sed "s|\.mat|_ranked.mat|" | sed "s|$VERBS_FEATURE_DIR|$VERBS_FEATURE_RANKED_DIR|" );
  if [ ! -s $verb_mat_rank ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"addpath('$SRC_DIR');" >> $CMDS_FILE
    printf "%s\n" "rank_verb('$verb_mat', '$verb_mat_rank'); quit\\\";" >> $CMDS_FILE;
  fi

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER} ${CMDS_FILE} ${CPU_CORE} exe 1 \n";
printf "rm -v ${CMDS_FILE}; \n"


