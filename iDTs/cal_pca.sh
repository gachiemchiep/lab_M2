#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

mkdir $PCA_SRC;

# make hog pca
if [ ! -s $HOG_PCA_RAW ]; then

  HOG_raws=$( find $HOGs_SRC -type f | shuf | head -n 5000 );

  for HOG_raw in ${HOG_raws[@]}; do
    shuf $HOG_raw | head -n 100 >> $HOG_PCA_RAW;
  done

fi

# make hof pca
if [ ! -s $HOF_PCA_RAW ]; then

  HOF_raws=$( find $HOFs_SRC -type f | shuf | head -n 5000 );

  for HOF_raw in ${HOF_raws[@]}; do
    shuf $HOF_raw | head -n 100 >> $HOF_PCA_RAW;
  done

fi

# make mbh pca
if [ ! -s $MBH_PCA_RAW ]; then

  MBH_raws=$( find $MBHs_SRC -type f | shuf | head -n 5000 );

  for MBH_raw in ${MBH_raws[@]}; do
    shuf $MBH_raw | head -n 100 >> $MBH_PCA_RAW;
  done

fi

echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_pca('$HOG_PCA_DICT','$HOG_PCA'); quit\" ;"
echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_pca('$HOF_PCA_DICT','$HOF_PCA'); quit\" ;"
echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_pca('$MBH_PCA_DICT','$MBH_PCA'); quit\" ;"


##################################### start shirnk raw hog, hof, mbh ###################
rm $CMDS_FILE

mkdir $HOGs_pca_SRC $HOFs_pca_SRC $MBHs_pca_SRC

# hog
HOG_raws=$( find $HOGs_SRC -type f );
for HOG_raw in ${HOG_raws[@]}; do

  HOG_pca=$( printf "$HOG_raw" | sed "s|$HOGs_SRC|$HOGs_pca_SRC|" );
  if [ ! -s  $HOG_pca ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "reduce_size('$HOG_raw', '$HOG_pca', '$HOG_PCA_DICT', '48'); quit\\\";" >> $CMDS_FILE;
  fi

done

# hof
HOF_raws=$( find $HOFs_SRC -type f );
for HOF_raw in ${HOF_raws[@]}; do

  HOF_pca=$( printf "$HOF_raw" | sed "s|$HOFs_SRC|$HOFs_pca_SRC|" );
  if [ ! -s  $HOF_pca ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "reduce_size('$HOF_raw', '$HOF_pca', '$HOF_PCA_DICT', '54'); quit\\\";" >> $CMDS_FILE;
  fi

done

# mbh
MBH_raws=$( find $MBHs_SRC -type f );
for MBH_raw in ${MBH_raws[@]}; do

  MBH_pca=$( printf "$MBH_raw" | sed "s|$MBHs_SRC|$MBHs_pca_SRC|" );
  if [ ! -s  $MBH_pca ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "reduce_size('$MBH_raw', '$MBH_pca', '$MBH_PCA_DICT', '96'); quit\\\";" >> $CMDS_FILE;
  fi

done

echo "perl ${EXE_CLUSTER} ${CMDS_FILE} ${CPU_CORE} exe 1 ";
