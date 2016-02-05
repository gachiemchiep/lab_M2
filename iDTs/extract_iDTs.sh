#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

rm $CMDS_FILE
AVI_FILES=($( find $AVI_SRC -type f -name "*avi" ));

for AVI_FILE in ${AVI_FILES[@]}; do

  iDTs_FILE=$( printf "$AVI_FILE" | sed "s|$AVI_SRC|$iDTs_SRC|" | sed "s|\.avi|\.txt|" );

  if [ ! -s $iDTs_FILE ]; then
    printf "%s\n" "cd $PWD;$PROG $AVI_FILE | sed s'/.$//' > $iDTs_FILE" >> $CMDS_FILE
  fi

done

echo "perl $EXE_CLUSTER ${CMDS_FILE} ${CPU_CORE} exe 1"
#rm -v $CMDS_FILE





