#!/bin/bash
### extract cnn feature base on given parameters
if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

printf "VIDS_LIST :\t $VIDS_LIST \n";
printf "OPFLOWS_LIST :\t $OPFLOWS_LIST \n";
printf "DEFAULT_NETWORK :\t $DEFAULT_NETWORK \n";
printf "MODEL :\t $MODEL \n";
printf "LAYER :\t $LAYER \n";
printf "TMP_DIR :\t $TMP_DIR \n";
printf "FEATURE_DIR :\t $FEATURE_DIR \n";

### check input params ###
if [ ! -d $TMP_DIR ]; then
  mkdir $TMP_DIR
fi

if [ ! -d $FEATURE_DIR ]; then
  mkdir $FEATURE_DIR
fi

##### merge opflows_list into leveldb ####
name=$( basename $OPFLOWS_LIST );
name_only="${name%.*}";

if [ ! -d ${OPFLOWS_LEVELDB} ]; then
  printf "Start mergeing\n";
  printf "$OPFLOWS_LIST \n";
  echo "python $MERGER $OPFLOWS_LIST ${OPFLOWS_LEVELDB} unshuffled";
else
  printf "${OPFLOWS_LEVELDB} is existed. Check wheter it was created before\n";
  #exit;
fi

exit

##### extracting features ############
### generate tmp network base on given parameters
network=$PWD/extract_features_net.txt
batch=125 # do not change this value

cat $DEFAULT_NETWORK | sed "s|OPFLOWS_LEVELDB|${OPFLOWS_LEVELDB}|" | sed "s|batch_count|$batch|" | sed "s|MEAN_FILE|$MEAN_FILE|" > ${network}.tmp
cat ${network}.tmp | sed "s|OPFLOWS_LEVELDB|${OPFLOWS_LEVELDB}|" | sed "s|batch_count|$batch|" > ${network}

rm ${network}.tmp;

STEP=$( wc -l < $OPFLOWS_LIST );

list_name_tmp=$( basename $VIDS_LIST );
list_name="${list_name_tmp%.*}";

FEATURE_LEVELDB=$( printf "$TMP_DIR/${list_name}_${LAYER}" );

if [ ! -d ${FEATURE_LEVELDB} ]; then
  ${EXTRACTOR} ${MODEL} $network ${LAYER} ${FEATURE_LEVELDB} $STEP leveldb GPU 1
fi

if [ ! -s ${FEATURE_LEVELDB}.txt.tmp ]; then
  ${READER} ${FEATURE_LEVELDB} ${FEATURE_LEVELDB}.txt.tmp;
fi

if [ ! -s ${FEATURE_LEVELDB}.txt ]; then
  # remove the leveldb key
  cut -d "," -f 2- ${FEATURE_LEVELDB}.txt.tmp > ${FEATURE_LEVELDB}.txt;
fi

##### split the feature text file and move rename #####
if [ ! -d ${TMP_DIR}/features ]; then
  mkdir ${TMP_DIR}/features
fi

if [ ! -d ${TMP_DIR}/features_tmp ]; then
  mkdir ${TMP_DIR}/features_tmp
fi

prefix=$( basename ${FEATURE_LEVELDB}.txt );
suffix=".txt";

feature_files_count=$( find ${FEATURE_DIR} -type f -name "*.txt" | wc -l );

cd  ${TMP_DIR}/features_tmp;
#split --suffix-length 6 --numeric-suffixes --lines 125 ${FEATURE_LEVELDB}.txt ${prefix}-

VIDS=($( cat $VIDS_LIST | tr "\n" " " | tr "\r" " " ));
FEATURE_FILES=($( find $PWD -type f -name "${prefix}-*" | sort ));

VIDS_count=${#VIDS[@]};
FEATURE_FILES_count=${#FEATURE_FILES[@]};

cd -;

CMDS_FILE=$PWD/extract_features.txt;
rm -v $CMDS_FILE;

mkdir $FEATURE_mat_DIR

for (( index=0; index<$VIDS_count; index++ )); do

 VID=${VIDS[$index]};
 FEATURE_src=${FEATURE_FILES[$index]};

 name_tmp=$( basename $VID );
 name="${name_tmp%.*}";
 FEATURE_dst=$( printf "${FEATURE_DIR}/${name}.txt" );

 printf "$VID \t $FEATURE_src \t $FEATURE_dst \n";
# mv $FEATURE_src $FEATURE_dst
 FEATURE_dst_mat=$( printf "${FEATURE_mat_DIR}/${name}.mat" );

 printf "%s"  "cd ${PWD}; /usr/local/bin/matlab2014a -nodisplay -r " >> ${CMDS_FILE};
 printf "%s\n" "  \\\"addpath('$SRC_DIR');convert('$FEATURE_dst', '$FEATURE_dst_mat'); quit;\\\" " >> ${CMDS_FILE};

done

printf "Run this command on im machine \n";
printf "perl ${EXE_CLUSTER} ${CMDS_FILE} ${CPU_CORE} exe 1 \n";
printf "rm -v ${CMDS_FILE}; \n";





