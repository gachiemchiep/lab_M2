#!/bin/python

import sys, os, leveldb, cv2, h5py
import numpy as np

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe


#### global params ####
MODES = ("shuffled", "unshuffled")
MERGE_COUNT = 100;  # bigger value come with bigger memory requirement


def check_argv(argv_):
    if not (len(argv_) == 4):
        print "Merge UCF-101 h5 into leveldb";
        print "Usage: python list_2_leveldb.py opflows_list(in hdf5 format) opflows_leveldb shuffled/unshuffled";
        sys.exit(0);
    else:
        list = argv_[1];
        if not (os.path.exists(list) or os.access(list, os.R_OK)):
            print "%s is not exist or unreadable" % (list);
            sys.exit(0);

        leveldb = argv_[2];
        if (os.path.exists(leveldb)):
            print "%s is exist or parent directory is unwriteable" % (leveldb);
            sys.exit(0);

        mode = argv_[3];
        if not mode in MODES:
            print "%s is not available mode" % (mode);
            print "Available mode is";
            print MODES;
            sys.exit(0);


def read_list(list_):
    h5_paths = [];

    with open(list_, "r") as fid:
        for line in fid:
            h5_path = line.replace("\n", "").replace("\r", "");
            if ((os.path.isfile(h5_path))):
                h5_paths.append(h5_path);
            else:
                print("%s is not a file \n" % (h5_path));

    fid.close();
    return (h5_paths);


def merge_opflows(argv_):
    print "merge_opflows"

    h5list = argv_[1];
    (h5_paths) = read_list(h5list);

    leveldb_path = argv_[2];

    is_shuffled = False;

    try:
        tmp = argv_[3];
        if (tmp == "shuffled"):
            is_shuffled = True;
        elif (tmp == "unshuffled"):
            is_shuffled = False;
        else:
            raise Exception('Invalid options');

    except Exception as err:
        print err;
        sys.exit(0);

    db = leveldb.LevelDB(leveldb_path, create_if_missing=True, error_if_exists=True);
    batch = leveldb.WriteBatch();
    db_key = 0;

    #
    if not ((len(h5_paths) % MERGE_COUNT) == 0):
        merge_time_count = int(len(h5_paths) / MERGE_COUNT) + 1;
    else:
        merge_time_count = int(len(h5_paths) / MERGE_COUNT);

    h5_fid = h5py.File(h5_paths[0], "r");
    h5_data = np.asarray(h5_fid['/data']);
    h5_fid.close();

    # blob.num, blob.channels, blob.height, blob.width
    # store data size
    data_count = h5_data.shape[0];
    data_channels = h5_data.shape[1];
    data_h = h5_data.shape[2];
    data_w = h5_data.shape[3];

    # merge part of the list
    for merge_time in range(merge_time_count):
        # go to nearly end of the list
        if (merge_time == (merge_time_count - 1)):
            MERGE_COUNT_LEFT = len(h5_paths) - (merge_time * MERGE_COUNT);
            data = np.zeros((data_count * MERGE_COUNT_LEFT, data_channels, data_h, data_w), dtype=np.uint8);
            labels = np.zeros((data_count * MERGE_COUNT_LEFT), dtype=np.uint8);
            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT;
            list_end = list_start + MERGE_COUNT_LEFT;
        # still have a lot of files
        else:
            data = np.zeros((data_count * MERGE_COUNT, data_channels, data_h, data_w), dtype=np.uint8);
            labels = np.zeros((data_count * MERGE_COUNT), dtype=np.uint8);

            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT;
            list_end = list_start + MERGE_COUNT;

        # read file content into memory
        for list_index in range(list_start, list_end):
            h5_path = h5_paths[list_index];

            h5_fid = h5py.File(h5_path, "r");
            h5_data = np.asarray(h5_fid['/data']);
            h5_labels_tmp = np.asarray(h5_fid['/label']);
            h5_labels = h5_labels_tmp.T;
            h5_fid.close();

            count_start = (list_index - list_start) * data_count;
            count_end = (list_index - list_start + 1) * data_count;  ### do not change this

            print("%s\t" % (h5_path));
            print("Merge :%d times\t List index: %d\t"
                  "Array start: %d\t end: %d" % (merge_time + 1, list_index, count_start, count_end));

            data[count_start:count_end, :, :, :] = h5_data[:, :, :, :];
            labels[count_start:count_end] = h5_labels[:];


        # start the shuffle here
        if is_shuffled:
            shuffle_keys = np.random.permutation(data.shape[0]);
        else:
            shuffle_keys = np.asarray(range(data.shape[0]));

        # now push into leveldb
        for index in range(data.shape[0]):

            part = data[shuffle_keys[index], :, :, :];

            datum = caffe.proto.caffe_pb2.Datum();
            datum.channels = part.shape[0];
            datum.height = part.shape[1];
            datum.width = part.shape[2];
            datum.label = int(labels[shuffle_keys[index]]);
            datum.data = part.tobytes();  # or .tostring() if numpy < 1.9

            # use 10 bit so that it can stretch to bigger data
            db_key = db_key + 1;
            db_key_str = '{:08}'.format(db_key)

            # The encode is only essential in Python 3
            batch.Put(db_key_str.encode('ascii'), datum.SerializeToString());

            # push per 2000 file
            if ((db_key % 2000) == 0) or (index == (data.shape[0] - 1)):
                # write batch
                print 'Processed %d line with datum format:' \
                      'channels: %d  height: %d  width: %d' \
                      % (db_key, datum.channels, datum.height, datum.width);
                db.Write(batch, sync=True);
                del batch
                batch = leveldb.WriteBatch();

            del part;

        del data
        del labels


def main():
    check_argv(sys.argv);
    merge_opflows(sys.argv);


if __name__ == "__main__":
    main()
