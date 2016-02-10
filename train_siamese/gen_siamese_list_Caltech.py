__author__ = 'gachiemchiep'

#!/bin/python

# generate similar/dissimilar dis for UCF-101

from os import listdir, walk
from os.path import isfile, join
import os, cv2
import numpy as np


IMAGE_DIR='/export/space2/vugia/Caltech/Caltech101/';

# positive: negative is not  1:1
# positive: megative = 1:16


SIM_COUNT_TRAIN = 100;
SIM_COUNT_TRAIN_ALL  =  SIM_COUNT_TRAIN * 100;
DISSIM_COUNT_TRAIN = SIM_COUNT_TRAIN * 100 * 16;  # DISSIM_COUNT_TRAIN = SIM_COUNT_TRAIN * verb_count
SIM_COUNT_TEST = 10;
SIM_COUNT_TEST_ALL = SIM_COUNT_TEST * 100;
DISSIM_COUNT_TEST = SIM_COUNT_TEST * 100 * 16;


OF_dir = IMAGE_DIR;

# generate 100 similar part for each verb
sim_pairs = [];

# which verb
verbs = [];

verbs = [];
for verb in listdir(OF_dir):
    verb_tmp = os.path.join(OF_dir, verb);
    if os.path.isdir(verb_tmp):
        verbs.append(verb_tmp);

verb_paths_all = [];
for verb in verbs:
    verb_paths = [];
    for verb_path in listdir(verb):
        verb_path_tmp = os.path.join(verb, verb_path);
        if os.path.isfile(verb_path_tmp) &  ("jpg" in verb_path_tmp):

            verb_paths.append(verb_path_tmp);
            verb_paths_all.append(verb_path_tmp);

    random_map = np.zeros([len(verb_paths), len(verb_paths)]);
    random_keys = np.random.permutation(len(verb_paths) * len(verb_paths));

    sim_count = 0;
    index = 0;
    while True:
        random_key = random_keys[index];
        random_row = int(random_key / random_map.shape[0]);
        random_col = random_key % random_map.shape[0]

        if not (random_row == random_col):
            verb_path_1 = verb_paths[random_row];
            verb_path_2 = verb_paths[random_col];

            tmp_str = '%s,%s,1' % (verb_path_1, verb_path_2);
            sim_pairs.append(tmp_str);
            sim_count = sim_count + 1;

        index = index + 1;
        if (sim_count >= (SIM_COUNT_TRAIN + SIM_COUNT_TEST)):
            break;

dissim_pairs = [];

random_map = np.zeros([len(verb_paths_all), len(verb_paths_all)]);
random_keys = np.random.permutation(len(verb_paths_all) * len(verb_paths_all));

dissim_count = 0;
index = 0;
while True:
    random_key = random_keys[index];
    random_row = int(random_key / random_map.shape[0]);
    random_col = random_key % random_map.shape[0]

    verb_path_1 = verb_paths_all[random_row];
    verb_path_2 = verb_paths_all[random_col];

    if not (verb_path_1 == verb_path_2):
        dissim_count = dissim_count + 1;

        tmp_str = '%s,%s,0' % (verb_path_1, verb_path_2);
        dissim_pairs.append(tmp_str);

    index = index + 1;
    if (dissim_count >= (DISSIM_COUNT_TRAIN + DISSIM_COUNT_TEST)):
        break;

print("Sim count %d" % (len(sim_pairs)));
print("Dissim count %d" % (len(dissim_pairs)));


train_file = "LIST/Caltech101_train.txt";
test_file = "LIST/Caltech101_test.txt";


train_fid = open(train_file, 'w');
test_fid = open(test_file, 'w');

sim_random_keys = np.random.permutation(len(sim_pairs));
dissim_random_keys = np.random.permutation(len(dissim_pairs));

for count in range(SIM_COUNT_TRAIN_ALL):
    train_fid.write('%s\n' % (sim_pairs[sim_random_keys[count]]));

for count in range(DISSIM_COUNT_TRAIN):
    train_fid.write('%s\n' % (dissim_pairs[dissim_random_keys[count]]));

train_fid.close();

for count in range(SIM_COUNT_TRAIN_ALL, SIM_COUNT_TRAIN_ALL + SIM_COUNT_TEST_ALL, 1):
    test_fid.write('%s\n' % (sim_pairs[sim_random_keys[count]]));
for count in range(DISSIM_COUNT_TRAIN, (DISSIM_COUNT_TRAIN + DISSIM_COUNT_TEST), 1):
    test_fid.write('%s\n' % (dissim_pairs[dissim_random_keys[count]]));

test_fid.close();
