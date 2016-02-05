#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

feature_count=$( wc -l < ${VIDS_LIST} );
name=$( basename ${VIDS_LIST});

CMDS_FILE=$PWD/cal_dists.txt;
rm -v $CMDS_FILE;

if [ ! -d $DIST_DIR ]; then
 mkdir $DIST_DIR;
fi

#for (( index=1; index<="${feature_count}"; index++ )); do
for (( index="${feature_count}"; index>=1; index-- )); do

  if [ ! -s ${DIST_DIR}/${name%.*}_${LAYER}_${index}.mat ]; then

    printf "%s"  "cd ${PWD}; /usr/local/bin/matlab2014a -nodisplay -r  \\\"addpath('$SRC_DIR');" >> ${CMDS_FILE};
    printf "%s\n" "  cal_dists('$PWD/${name%.*}_${LAYER}.mat', '${DIST_DIR}/${name%.*}_${LAYER}_${index}.mat',$index); quit;\\\" " >> ${CMDS_FILE};

  fi

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER} ${CMDS_FILE} ${CPU_CORE} exe 1 \n";
printf "rm -v ${CMDS_FILE}; \n";