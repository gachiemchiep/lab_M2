#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

if [ ! -d $HOGs_SRC ]; then
  mkdir -v $HOGs_SRC;
fi

rm $CMDS_FILE

iDTs=($( find $iDTs_SRC -type f ));

for iDT in ${iDTs[@]}; do

  HOG=$( printf "$iDT" | sed "s|$iDTs_SRC|$HOGs_SRC|" );
  HOF=$( printf "$iDT" | sed "s|$iDTs_SRC|$HOFs_SRC|" );
  MBH=$( printf "$iDT" | sed "s|$iDTs_SRC|$MBHs_SRC|" );

  if [ ! -s $HOG ]; then
    printf "%s\n" "cd $PWD; awk -F ',' '{if ($7 == 1.0) print}' | cut -d ',' -f 41-136 $iDT > $HOG " >> $CMDS_FILE;
  fi

  if [ ! -s $HOF ]; then
    printf "%s\n" "cd $PWD; awk -F ',' '{if ($7 == 1.0) print}' | cut -d ',' -f 137-244 $iDT > $HOG " >> $CMDS_FILE;
  fi

  if [ ! -s $MBH ]; then
    printf "%s\n" "cd $PWD; awk -F ',' '{if ($7 == 1.0) print}' | cut -d ',' -f 245-436 $iDT > $HOG " >> $CMDS_FILE;
  fi

done

echo "perl $EXE_CLUSTER ${CMDS_FILE} ${CPU_CORE} exe 1"
#rm -v $CMDS_FILE