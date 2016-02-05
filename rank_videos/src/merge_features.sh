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

# merge into biggest
find $FEATURE_mat_DIR -type f -name "*.mat" | sort > feature_mats_list.txt;
name=$( basename ${VIDS_LIST});

# should only merge the path of mat file,
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');merge_features('$VIDS_LIST','$OPFLOWS_LIST','$PWD/feature_mats_list.txt','$PWD/${name%.*}_${LAYER}.mat'); quit";
# sort features vectors for each verbs and save inside $VERBS_FEATURE_DIR
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');sort_features('$PWD/${name%.*}_${LAYER}.mat', '$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_DIR'); quit";

# show visual rank
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');show_VisualRank('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted.txt'); quit";


# calculate tree with visual ranked
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.3.fig', 0.3); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.4.fig', 0.4); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.5.fig', 0.5); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.6.fig', 0.6); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.7.fig', 0.7); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.8.fig', 0.8); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_0.9.fig', 0.9); quit";
/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR', '$PWD/${name%.*}_${LAYER}_sorted_ranked_1.0.fig', 1.0); quit";

#/usr/local/bin/matlab2014a -nodisplay -r "addpath('$SRC_DIR');cal_trees_ranked_2('$PWD/${name%.*}_${LAYER}_sorted.mat', '$VERBS_FEATURE_RANKED_DIR_2', '$PWD/${name%.*}_${LAYER}_sorted_ranked_2.fig'); quit";

