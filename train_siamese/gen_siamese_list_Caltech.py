__author__ = 'gachiemchiep'

#!/bin/python

# generate similar/dissimilar dis for UCF-101

from os import listdir, walk
from os.path import isfile, join
import os, cv2
import numpy as np


IMAGE_DIR='/export/data/corel/Caltech256/';

SIM_COUNT_TRAIN = 30;
DISSIM_COUNT_TRAIN = SIM_COUNT_TRAIN * 20;  # DISSIM_COUNT_TRAIN = SIM_COUNT_TRAIN * verb_count
SIM_COUNT_TEST = 10;
DISSIM_COUNT_TEST = SIM_COUNT_TEST * 20;


OF_dir = IMAGE_DIR;

# generate 100 similar part for each verb
sim_pairs = [];

# which verb
verbs = [];

verbs = [];
for verb in listdir(OF_dir)[1:21]:
    verb_tmp = os.path.join(OF_dir, verb);
    if os.path.isdir(verb_tmp):
        verbs.append(verb_tmp);

verb_OFs_all = [];
for verb in verbs:
    verb_OFs = [];
    for verb_OF in listdir(verb):
        verb_OF_tmp = os.path.join(verb, verb_OF);
        if os.path.isfile(verb_OF_tmp) &  ("jpg" in verb_OF_tmp):

            verb_OFs.append(verb_OF_tmp);
            verb_OFs_all.append(verb_OF_tmp);

    random_map = np.zeros([len(verb_OFs), len(verb_OFs)]);
    random_keys = np.random.permutation(len(verb_OFs) * len(verb_OFs));

    sim_count = 0;
    index = 0;
    while True:
        random_key = random_keys[index];
        random_row = int(random_key / random_map.shape[0]);
        random_col = random_key % random_map.shape[0]

        if not (random_row == random_col):
            verb_OF_1 = verb_OFs[random_row];
            verb_OF_2 = verb_OFs[random_col];

            tmp_str = '%s,%s,1' % (verb_OF_1, verb_OF_2);
            sim_pairs.append(tmp_str);
            sim_count = sim_count + 1;

        index = index + 1;
        if (sim_count >= (SIM_COUNT_TRAIN + SIM_COUNT_TEST)):
            break;

print len(verb_OFs_all);

dissim_pairs = [];

random_map = np.zeros([len(verb_OFs_all), len(verb_OFs_all)]);
random_keys = np.random.permutation(len(verb_OFs_all) * len(verb_OFs_all));

dissim_count = 0;
index = 0;
while True:
    random_key = random_keys[index];
    random_row = int(random_key / random_map.shape[0]);
    random_col = random_key % random_map.shape[0]

    verb_OF_1 = verb_OFs_all[random_row];
    verb_OF_2 = verb_OFs_all[random_col];

    if not (verb_OF_1 == verb_OF_2):
        dissim_count = dissim_count + 1;

        tmp_str = '%s,%s,0' % (verb_OF_1, verb_OF_2);
        dissim_pairs.append(tmp_str);

    index = index + 1;
    if (dissim_count >= (DISSIM_COUNT_TRAIN + DISSIM_COUNT_TEST)):
        break;

train_file = "Caltech256_train.txt";
test_file = "Caltech256_test.txt";

print len(sim_pairs);
print len(dissim_pairs);

train_fid = open(train_file, 'w');
test_fid = open(test_file, 'w');

random_keys = np.random.permutation(len(sim_pairs));
for count in range(DISSIM_COUNT_TRAIN):
    train_fid.write('%s\n' % (sim_pairs[random_keys[count]]));
    train_fid.write('%s\n' % (dissim_pairs[random_keys[count]]));

train_fid.close();

for count in range(DISSIM_COUNT_TRAIN, (DISSIM_COUNT_TRAIN + DISSIM_COUNT_TEST), 1):
    test_fid.write('%s\n' % (sim_pairs[random_keys[count]]));
    test_fid.write('%s\n' % (dissim_pairs[random_keys[count]]));

test_fid.close();
