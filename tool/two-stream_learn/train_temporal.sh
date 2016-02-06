#!/usr/bin/env bash

mkdir -v MODEL
mkdir -v LOG

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

echo "$DEFAULT_NETWORK"

cat $DEFAULT_NETWORK | sed "s|TEST_LEVELDB|$TEST_LEVELDB|" | sed "s|TRAIN_LEVELDB|$TRAIN_LEVELDB|" > ${NETWORK}.tmp
cat ${NETWORK}.tmp | sed "s|TRAIN_BATCH_COUNT|$TRAIN_BATCH_COUNT|" | sed "s|TEST_BATCH_COUNT|$TEST_BATCH_COUNT|" > ${NETWORK}.tmp2;
cat ${NETWORK}.tmp2 | sed "s|MEAN_FILE|$MEAN_FILE|g" > ${NETWORK};

rm ${NETWORK}.tmp ${NETWORK}.tmp2

######## 1st stage : 0-50k:0.01,50k-70:0.001 ##################
cat $DEFAULT_SOLVER | sed "s|NETWORK|$NETWORK|" | sed "s|SNAPSHOT|$SNAPSHOT|" > $SOLVER;
time_stamp=$( date +"%y%m%d%H" )
LOG=$( printf "$NETWORK" | sed "s|\.txt|_1st_${time_stamp}.log|" | sed "s|NET|LOG|" );
${CAFFE} train --solver=$SOLVER  -gpu 1,0 2>&1 | tee ${LOG};

######### 2nd stage 20k: 0.0001 ######################
cat $DEFAULT_SOLVER_2 | sed "s|NETWORK|$NETWORK|" | sed "s|SNAPSHOT|$SNAPSHOT_2|" > $SOLVER_2;
time_stamp=$( date +"%y%m%d%H" )
LOG=$( printf "$NETWORK" | sed "s|\.txt|_2nd_${time_stamp}.log|" | sed "s|NET|LOG|" );
${CAFFE} train --solver=$SOLVER_2 --weights=$WEIGHTS  -gpu 1,0 2>&1 | tee ${LOG};
