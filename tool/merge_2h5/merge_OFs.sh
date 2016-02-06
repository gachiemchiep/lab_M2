#!/bin/bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

DIRS=$( find $SRC_DIR/* -mindepth 2 -maxdepth 2 -type d );

for DIR in ${DIRS[@]}; do

  printf "$DIR \t"

  H5_FILE=$( printf "$DIR" | sed "s|$SRC_DIR|$DST_DIR|" | sed "s|$|\.h5|" );
  if [ ! -s $H5_FILE ]; then

    python $MERGER $DIR $STACKED_COUNT $H5_FILE noncrop $SAMPLING_COUNT;
    
    printf "$H5_FILE     merged"

  fi

  printf "\n";

#done

done
