#!/usr/bin/env bash

if [ ! $# -eq 1 ]; then
  printf "%s\n" "Usage: bash $0 configuration_file(../test.cfg)"
  exit 0
fi

printf "Reading configuration  \n";
source $1;

for LOG_FILE in ${LOG_FILES[@]}; do
printf "LOG: $LOG_FILE \n";
# Training losss
cat $LOG_FILE | grep "Train net output" | rev | cut -d " " -f 2 | rev | tail -n +2 > train_loss.txt;
count=$( wc -l < train_loss.txt);
rm train_iter.txt;
for (( index=1; index<=$count; index++ )); do
    let iteration=$index*${TRAIN_STEP};
    printf "$iteration\n" >> train_iter.txt;
done

# testing loss
cat $LOG_FILE | grep "Test net output" | rev | cut -d " " -f 2 | rev | tail -n +2 > test_loss.txt;
rm test_iter.txt;
count=$( wc -l < test_loss.txt);
for (( index=1; index<=$count; index++ )); do
    let iteration=$index*${TEST_STEP};
    printf "$iteration\n" >> test_iter.txt;
done

paste -d " " train_iter.txt train_loss.txt test_iter.txt test_loss.txt > plot.dat

rm train_iter.txt train_loss.txt test_iter.txt test_loss.txt

LOG_NAME=$( basename ${LOG_FILE} );
PLOT_NAME=$( printf "$LOG_NAME" | sed "s|\.log|\.png|" );

gnuplot <<- EOF
    set xlabel "Iterations time"
    set ylabel "Loss"
    set logscale y
    set term png size 2048,1536
    set tics font ", 20"
    set key font ",30"
    set output "${PLOT_NAME}"
    set style line 1 lc rgb '#0060ad' lt 1 lw 1 pt 1 ps 0   # --- blue
    #plot "plot.dat" using 1:2 title "Train_loss" with lines smooth bezier, '' using 3:4;
    #plot "plot.dat" using 1:2 title "Train_loss" with lines smooth bezier;
    plot "plot.dat" using 1:2 title "Train_loss" with lines smooth bezier,'' using 3:4 title "Test_loss" with lines smooth bezier;
    plot "plot.dat" using 1:2 title "Train_loss" with lines,'' using 3:4 title "Test_loss" with lines;
    exit;
EOF

done