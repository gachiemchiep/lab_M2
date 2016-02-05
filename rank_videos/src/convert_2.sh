#!/bin/bash
### extract cnn feature base on given parameters
if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

CMDS_FILE=$PWD/extract_features.txt;
rm -v $CMDS_FILE;

if [ ! "$SOURCE_FEATURE" ]; then
  printf "SOURCE_FEATURE is not set\n"
  printf "Please edit configure file\n"
  exit;
fi

FEATURES=($( find $SOURCE_FEATURE -type f ) );

mkdir $FEATURE_mat_DIR

for FEATURE in ${FEATURES[@]}; do

  FEATURE_NAME=$( basename $FEATURE );

  FEATURE_dst=$( printf "${FEATURE_mat_DIR}/${FEATURE_NAME}" );

  if [ ! -s $FEATURE_dst ]; then

    printf "%s"  "cd ${PWD}; /usr/local/bin/matlab2014a -nodisplay -r " >> ${CMDS_FILE};
    printf "%s\n" "  \\\"addpath('$SRC_DIR');convert_2('$FEATURE', '$FEATURE_dst'); quit;\\\" " >> ${CMDS_FILE};

  fi

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER} ${CMDS_FILE} ${CPU_CORE} exe 1 \n";
printf "rm -v ${CMDS_FILE}; \n";





