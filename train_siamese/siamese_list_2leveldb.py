__author__ = 'gachiemchiep'

# !/bin/python

import sys, os, leveldb, cv2, h5py
import numpy as np

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe


#### global params ####
MODES = ("image", "opflows")
THRESHOLD_VAL = 64;
MERGE_COUNT = 50;  # bigger value come with bigger memory requirement


def check_argv(argv_):
    if (len(argv_) < 4):
        print "Generate leveldb data to train siamse net"
        print "Usage: python list_2_leveldb.py h5list output_leveldb image\n" \
              "Or \n" \
              "python list_2_leveldb.py h5list output_leveldb opflows shuffled/unshuffled threshold/raw";
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

            # check each


def read_list(list_):
    patch_1_paths = [];
    patch_2_paths = [];
    similarities = [];

    with open(list_, "r") as fid:
        for line in fid:

            contains = line.replace('\n', '').split(',');

            patch_1_path = contains[0];
            patch_2_path = contains[1];
            if ((os.path.isfile(patch_1_path)) & (os.path.isfile(patch_2_path))):
                patch_1_paths.append(patch_1_path);
                patch_2_paths.append(patch_2_path);
                similarities.append(int(contains[2]));

            else:
                print("%s\t%s\n" % (patch_1_path, patch_2_path));

    fid.close();
    return (patch_1_paths, patch_2_paths, similarities);


def merge_imgs(argv_):
    print "merge_imgs"

    MERGE_COUNT_img = MERGE_COUNT * 100;

    pair_list = argv_[1];
    (patch_1_paths, patch_2_paths, similarities) = read_list(pair_list);

    leveldb_path = argv_[2];

    db = leveldb.LevelDB(leveldb_path, create_if_missing=True, error_if_exists=True);
    batch = leveldb.WriteBatch();

    db_key = 0;

    if not ((len(patch_1_paths) % MERGE_COUNT_img) == 0):
        merge_time_count = int(len(patch_1_paths) / MERGE_COUNT_img) + 1;
    else:
        merge_time_count = int(len(patch_1_paths) / MERGE_COUNT_img);

    # default size: height: 256 width: 340

    im_1_raw = cv2.imread(patch_1_paths[0], cv2.COLOR_RGB2BGR);
    im_1 = cv2.resize(im_1_raw, (340, 256))
    im_1_datum = np.transpose(im_1, [2, 0, 1]);  # h x w x channel -> channel x h x w

    # store data size
    data_count = 1;
    data_channel = im_1_datum.shape[0];
    data_h = im_1_datum.shape[1];
    data_w = im_1_datum.shape[2];

    # merge part of the list
    for merge_time in range(merge_time_count):

        # go to nearly end of the list
        if (merge_time == (merge_time_count - 1)):
            MERGE_COUNT_img_LEFT = len(patch_1_paths) - (merge_time * MERGE_COUNT_img);
            data_1 = np.zeros((data_count * MERGE_COUNT_img_LEFT, data_channel, data_h, data_w), dtype=np.uint8);
            data_2 = np.zeros((data_count * MERGE_COUNT_img_LEFT, data_channel, data_h, data_w), dtype=np.uint8);
            data_sims = np.zeros((data_count * MERGE_COUNT_img_LEFT), dtype=np.uint8);
            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT_img;
            list_end = list_start + MERGE_COUNT_img_LEFT;
        # still have a lot of files
        else:
            data_1 = np.zeros((data_count * MERGE_COUNT_img, data_channel, data_h, data_w), dtype=np.uint8);
            data_2 = np.zeros((data_count * MERGE_COUNT_img, data_channel, data_h, data_w), dtype=np.uint8);
            data_sims = np.zeros((data_count * MERGE_COUNT_img), dtype=np.uint8);

            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT_img;
            list_end = list_start + MERGE_COUNT_img;

        # read from files into memory
        for list_index in range(list_start, list_end):

            similarity = similarities[list_index];
            print('%s    %s' %(patch_1_paths[list_index], patch_2_paths[list_index]))
            # im_1_raw = cv2.imread(patch_1_paths[list_index], cv2.COLOR_RGB2BGR);
            # im_2_raw = cv2.imread(patch_2_paths[list_index], cv2.COLOR_RGB2BGR);

            im_1_raw = cv2.imread(patch_1_paths[list_index]);
            im_2_raw = cv2.imread(patch_2_paths[list_index]);


            im_1 = cv2.resize(im_1_raw, (340, 256))
            im_2 = cv2.resize(im_2_raw, (340, 256))

            im_1_datum = np.transpose(im_1, [2, 0, 1]);
            im_2_datum = np.transpose(im_2, [2, 0, 1]);

            count_start = (list_index - list_start) * data_count;
            count_end = (list_index - list_start + 1) * data_count;  ### do not change this

            data_1[count_start:count_end, :, :, :] = im_1_datum[:, :, :];
            data_2[count_start:count_end, :, :, :] = im_2_datum[:, :, :];

            # print("Merge :%d times\t List index: %d\t"
            #       "Array start: %d\t end: %d" % (merge_time + 1, list_index, count_start, count_end));

            data_sims[count_start:count_end] = similarity;

        # now push into leveldb
        for index in range(data_1.shape[0]):

            part_1 = data_1[index, :, :, :];
            part_2 = data_2[index, :, :, :];
            data_pair = np.asarray([part_1, part_2]);

            datum = caffe.proto.caffe_pb2.Datum();
            datum.channels = part_1.shape[0] * 2;
            datum.height = part_1.shape[1];
            datum.width = part_1.shape[2];
            datum.label = int(data_sims[index]);
            datum.data = data_pair.tobytes();  # or .tostring() if numpy < 1.9

            # use 10 bit so that it can stretch to bigger data
            db_key = db_key + 1;
            db_key_str = '{:08}'.format(db_key)

            # The encode is only essential in Python 3
            batch.Put(db_key_str.encode('ascii'), datum.SerializeToString());

            # push per 1000 file
            if ((db_key % 1000) == 0) or (index == (data_1.shape[0] - 1)):
                # write batch
                print 'Processed %d line with datum format:' \
                      'channels: %d  height: %d  width: %d' \
                      % (db_key, datum.channels, datum.height, datum.width);
                db.Write(batch, sync=True);
                del batch
                batch = leveldb.WriteBatch();

            del part_1;
            del part_2;

        del data_1
        del data_2
        del data_sims


def merge_opflows(argv_):
    print "merge_opflows"

    pair_list = argv_[1];
    (h5_1_paths, h5_2_paths, similarities) = read_list(pair_list);

    leveldb_path = argv_[2];

    is_shuffled = False;
    is_threshold = False;

    try:
        tmp = argv_[4];
        if (tmp == "shuffled"):
            is_shuffled = True;
        elif (tmp == "unshuffled"):
            is_shuffled = False;
        else:
            raise Exception('Invalid options');

        tmp2 = argv_[5];
        if (tmp2 == "threshold"):
            is_threshold = True;
        elif (tmp2 == "raw"):
            is_threshold = False;
        else:
            raise Exception('Invalid options');

    except Exception as err:
        print err;
        sys.exit(0);

    db = leveldb.LevelDB(leveldb_path, create_if_missing=True, error_if_exists=True);
    batch = leveldb.WriteBatch();
    db_key = 0;

    #
    if not ((len(h5_1_paths) % MERGE_COUNT) == 0):
        merge_time_count = int(len(h5_1_paths) / MERGE_COUNT) + 1;
    else:
        merge_time_count = int(len(h5_1_paths) / MERGE_COUNT);

    h5_1_fid = h5py.File(h5_1_paths[0], "r");
    h5_1_data = np.asarray(h5_1_fid['/data']);
    h5_1_fid.close();

    print h5_1_data.shape

    # store data size
    data_count = h5_1_data.shape[0];
    data_channels = h5_1_data.shape[1];
    data_h = h5_1_data.shape[2];
    data_w = h5_1_data.shape[3];

    print h5_1_data.shape

    # merge part of the list
    for merge_time in range(merge_time_count):
        # go to nearly end of the list
        if (merge_time == (merge_time_count - 1)):
            MERGE_COUNT_LEFT = len(h5_1_paths) - (merge_time * MERGE_COUNT);
            data_1 = np.zeros((data_count * MERGE_COUNT_LEFT, data_channels, data_h, data_w), dtype=np.uint8);
            data_2 = np.zeros((data_count * MERGE_COUNT_LEFT, data_channels, data_h, data_w), dtype=np.uint8);
            data_sims = np.zeros((data_count * MERGE_COUNT_LEFT), dtype=np.uint8);
            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT;
            list_end = list_start + MERGE_COUNT_LEFT;
        # still have a lot of files
        else:
            data_1 = np.zeros((data_count * MERGE_COUNT, data_channels, data_h, data_w), dtype=np.uint8);
            data_2 = np.zeros((data_count * MERGE_COUNT, data_channels, data_h, data_w), dtype=np.uint8);
            data_sims = np.zeros((data_count * MERGE_COUNT), dtype=np.uint8);

            # which part of the list is selected
            list_start = merge_time * MERGE_COUNT;
            list_end = list_start + MERGE_COUNT;

        # read file content into memory
        for list_index in range(list_start, list_end):
            h5_1 = h5_1_paths[list_index];
            h5_2 = h5_2_paths[list_index];
            similarity = int(similarities[list_index]);

            h5_1_fid = h5py.File(h5_1, "r");
            h5_1_data = np.asarray(h5_1_fid['/data']);
            h5_1_fid.close();

            h5_2_fid = h5py.File(h5_2, "r");
            h5_2_data = np.asarray(h5_2_fid['/data']);
            h5_2_fid.close();

            count_start = (list_index - list_start) * data_count;
            count_end = (list_index - list_start + 1) * data_count;  ### do not change this

            print("%s\t%s\t%d" % (h5_1, h5_2, similarity));
            print("Merge :%d times\t List index: %d\t"
                  "Array start: %d\t end: %d" % (merge_time + 1, list_index, count_start, count_end));

            data_1[count_start:count_end, :, :, :] = h5_1_data[:, :, :, :];
            data_2[count_start:count_end, :, :, :] = h5_2_data[:, :, :, :];
            data_sims[count_start:count_end] = similarity;


        # start the shuffle here
        if is_shuffled:
            shuffle_keys = np.random.permutation(data_1.shape[0]);
        else:
            shuffle_keys = np.asarray(range(data_1.shape[0]));

        # now push into leveldb
        for index in range(data_1.shape[0]):

            part_1 = data_1[shuffle_keys[index], :, :, :];
            part_2 = data_2[shuffle_keys[index], :, :, :];

            #
            # if is_threshold:
            #    part_1[np.where(part_1 >= THRESHOLD_VAL)] = 255;
            #    part_2[np.where(part_2 >= THRESHOLD_VAL)] = 255;

            data_pair = np.concatenate([part_1, part_2], axis=0);

            datum = caffe.proto.caffe_pb2.Datum();
            datum.channels = data_pair.shape[0];
            datum.height = data_pair.shape[1];
            datum.width = data_pair.shape[2];
            datum.label = int(data_sims[shuffle_keys[index]]);
            datum.data = data_pair.tobytes();  # or .tostring() if numpy < 1.9

            # use 10 bit so that it can stretch to bigger data
            db_key = db_key + 1;
            db_key_str = '{:08}'.format(db_key)

            # The encode is only essential in Python 3
            batch.Put(db_key_str.encode('ascii'), datum.SerializeToString());

            # push per 2000 file
            if ((db_key % 2000) == 0) or (index == (data_1.shape[0] - 1)):
                # write batch
                print 'Processed %d line with datum format:' \
                      'channels: %d  height: %d  width: %d' \
                      % (db_key, datum.channels, datum.height, datum.width);
                db.Write(batch, sync=True);
                del batch
                batch = leveldb.WriteBatch();

            del part_1;
            del part_2;

        del data_1
        del data_2
        del data_sims


ACTIONS = {'image': merge_imgs, 'opflows': merge_opflows};


def main():
    check_argv(sys.argv);

    pair_list = sys.argv[1];
    (patch_1_paths, patch_2_paths, similarities) = read_list(pair_list);

    leveldb_path = sys.argv[2];
    mode = sys.argv[3];

    ACTIONS[mode](sys.argv);


if __name__ == "__main__":
    main()
