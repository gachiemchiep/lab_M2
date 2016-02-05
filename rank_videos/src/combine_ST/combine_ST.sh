#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

echo "$FEATURE_mat_S_DIR"
echo "$FEATURE_mat_T_DIR"

spatial_mats=($( find $FEATURE_mat_S_DIR -type f | sort ));
temporal_mats=($( find $FEATURE_mat_T_DIR -type f | sort ));

mkdir  $TMP_DIR $FEATURE_mat_DIR

CMDS_FILE=$PWD/conbine_ST.txt
rm $CMDS_FILE;

MAX="${#spatial_mats[@]}";

for (( index=1; index<=$MAX; index++)); do

  ST_mat=$( printf "${spatial_mats[$index]}" | sed "s|$FEATURE_mat_S_DIR|$FEATURE_mat_DIR|" );
  if [ ! -s $ST_mat ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"addpath('$SRC_DIR');" >> $CMDS_FILE
    printf "%s\n" "combine_ST('${spatial_mats[$index]}', '${temporal_mats[$index]}', '$ST_mat'); quit\\\";" >> $CMDS_FILE;
  fi

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER_2} ${CMDS_FILE} exe ${CPU_CORE} 1 $PWD 70 82 6000 1 \n";
printf "rm -v ${CMDS_FILE}; \n"