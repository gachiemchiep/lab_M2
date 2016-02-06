#!/usr/bin/env bash
# extract optical flows for aslan

# /host/space2/vugia/dense_flow
# ./denseFlow_gpu -f test.avi -x tmp/flow_x -y tmp/flow_x -i tmp/image -b 20 -t 1 -d 0 -s 1

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

AVI_FILES=$( cat $AVI_LIST);

for AVI_FILE in ${AVI_FILES[@]}; do

  AVI_NAME=$( basename $AVI_FILE | sed "s|\.avi||" );

  printf "$AVI_NAME \t"

  file_x=$DST_DIR/${AVI_NAME}/${X_PREFIX}
  file_y=$DST_DIR/${AVI_NAME}/${Y_PREFIX}
  file_i=$DST_DIR/${AVI_NAME}/${I_PREFIX}

  if [ ! -d $DST_DIR/${AVI_NAME} ]; then
    mkdir $DST_DIR/${AVI_NAME}
    $DENSE_FLOW -f $AVI_FILE -x $file_x -y $file_y -i $file_i -b 20 -t $TYPE -d $DEVICE -s 1
  fi

  printf "$DST_DIR/${AVI_NAME}  done\n"

done
