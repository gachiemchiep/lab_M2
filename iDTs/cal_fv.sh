#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

mkdir $FV_SRC

# make hog fv raw
if [ ! -s $HOG_FV_RAW ]; then

  HOGs_pca_raws=$( find $HOGs_pca_SRC -type f | shuf | head -n 8000 );

  for HOGs_pca_raw in ${HOGs_pca_raws[@]}; do
    shuf $HOGs_pca_raw | head -n 32 >> $HOG_FV_RAW;
  done

fi

# make hof fv raw
if [ ! -s $HOF_FV_RAW ]; then

  HOFs_pca_raws=$( find $HOFs_pca_SRC -type f | shuf | head -n 8000 );

  for HOFs_pca_raw in ${HOFs_pca_raws[@]}; do
    shuf $HOFs_pca_raw | head -n 32 >> $HOF_FV_RAW;
  done

fi

# make hog fv raw
if [ ! -s $MBH_FV_RAW ]; then

  MBHs_pca_raws=$( find $MBHs_pca_SRC -type f | shuf | head -n 8000 );

  for MBHs_pca_raw in ${MBHs_pca_raws[@]}; do
    shuf $MBHs_pca_raw | head -n 32 >> $MBH_FV_RAW;
  done

fi

echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_fv_dict('$HOG_FV_RAW','$HOG_FV_DICT'); quit\" ;"
echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_fv_dict('$HOF_FV_RAW','$HOF_FV_DICT'); quit\" ;"
echo "  /usr/local/bin/matlab2014a -nodisplay -r \"addpath('$PWD');cal_fv_dict('$MBH_FV_RAW','$MBH_FV_DICT'); quit\" ;"

##################################### start calculating hog, hof, mbh fisher vectors ###################
rm $CMDS_FILE

mkdir $HOGs_fv_SRC $HOFs_fv_SRC $MBHs_fv_SRC

# hog
HOG_pca_raws=$( find $HOGs_pca_SRC -type f );
for HOG_pca_raw in ${HOG_pca_raws[@]}; do

  HOG_fv=$( printf "$HOG_pca_raw" | sed "s|$HOGs_pca_SRC|$HOGs_fv_SRC|" | sed "s|\.txt|\.mat|" );
  if [ ! -s  $HOG_fv ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "cal_fv('$HOG_pca_raw', '$HOG_fv', '$HOG_FV_DICT'); quit\\\";" >> $CMDS_FILE;
  fi

done

# hof
HOF_pca_raws=$( find $HOFs_pca_SRC -type f );
for HOF_pca_raw in ${HOF_pca_raws[@]}; do

  HOF_fv=$( printf "$HOF_pca_raw" | sed "s|$HOFs_pca_SRC|$HOFs_fv_SRC|" | sed "s|\.txt|\.mat|" );
  if [ ! -s  $HOF_fv ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "cal_fv('$HOF_pca_raw', '$HOF_fv', '$HOF_FV_DICT'); quit\\\";" >> $CMDS_FILE;
  fi

done

# mbh
MBH_pca_raws=$( find $MBHs_pca_SRC -type f );
for MBH_pca_raw in ${MBH_pca_raws[@]}; do

  MBH_fv=$( printf "$MBH_pca_raw" | sed "s|$MBHs_pca_SRC|$MBHs_fv_SRC|" | sed "s|\.txt|\.mat|" );
  if [ ! -s  $MBH_fv ]; then
    printf "%s" "cd $PWD; /usr/local/bin/matlab2014a -nodisplay -r \\\"" >> $CMDS_FILE
    printf "%s\n" "cal_fv('$MBH_pca_raw', '$MBH_fv', '$MBH_FV_DICT'); quit\\\";" >> $CMDS_FILE;
  fi

done
