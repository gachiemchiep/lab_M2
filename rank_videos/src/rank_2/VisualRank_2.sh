#!/usr/bin/env bash
# rank all the features vectors and select top 500 as representative features

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

mkdir $VERBS_FEATURE_DIR_2 $VERBS_FEATURE_RANKED_DIR_2
name=$( basename $VIDS_LIST );
# sort features vectors for each verbs and save inside $VERBS_FEATURE_DIR
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');sort_features_2('$PWD/${name%.*}_${LAYER}.mat', '$PWD/${name%.*}_${LAYER}_sorted_2.mat', '$VERBS_FEATURE_DIR_2'); quit";

CMDS_FILE=$PWD/VisualRank_2.txt
rm $CMDS_FILE;

verb_mats=$( find $VERBS_FEATURE_DIR_2 -type f -name "*.mat" -not -name "*_ranked.mat" );

if [ ! -d $VERBS_FEATURE_DIR_2 ]; then
  mkdir $VERBS_FEATURE_DIR_2 $VERBS_FEATURE_RANKED_DIR_2;
fi

for verb_mat in ${verb_mats[@]}; do

  verb_mat_rank=$( printf "$verb_mat" | sed "s|\.mat|_ranked.mat|" | sed "s|$VERBS_FEATURE_DIR_2|$VERBS_FEATURE_RANKED_DIR_2|" );
  if [ ! -s $verb_mat_rank ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"addpath('$SRC_DIR');" >> $CMDS_FILE
    printf "%s\n" "rank_verb('$verb_mat', '$verb_mat_rank'); quit\\\";" >> $CMDS_FILE;
  fi

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER_2} ${CMDS_FILE} exe ${CPU_CORE} 1 $PWD 70 82 6000 1 \n";
printf "rm -v ${CMDS_FILE}; \n"


