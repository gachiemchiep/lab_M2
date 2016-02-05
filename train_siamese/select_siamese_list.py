#!/bin/python

import sys, os, leveldb, cv2, h5py
import numpy as np

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe


#### global params ####
MERGE_COUNT = 50;  # bigger value come with bigger memory requirement

def check_argv(argv_):
    if not (len(argv_) == 6):
        print "Usage python %s network trained_model mean_file test_h5_list output_file" % (argv_[0])
        sys.exit(0);
    else:
        network = argv_[1];
        if not (os.path.exists(network) or os.access(network, os.R_OK)):
            print "Network:  %s is not exist or unreadable" % (network);
            sys.exit(0);

        trained_model = argv_[2];
        if not (os.path.exists(trained_model) or os.access(trained_model, os.R_OK)):
            print "Trained_model:  %s is not exist or unreadable" % (trained_model);
            sys.exit(0);

        mean_file = argv_[3];
        if not (os.path.exists(mean_file) or os.access(mean_file, os.R_OK)):
            print "mean_file:  %s is not exist or unreadable" % (mean_file);
            sys.exit(0);

        test_h5_list = argv_[4];
        if not (os.path.exists(test_h5_list) or os.access(test_h5_list, os.R_OK)):
            print "test_h5_list:  %s is not exist or unreadable" % (test_h5_list);
            sys.exit(0);

        output_file = argv_[5];
        if (os.path.exists(output_file)):
            print "%s will be rewrite" % (output_file);


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


def init():

    caffe.set_device(1);
    caffe.set_mode_gpu();

def check_pair(h5_path_1, h5_path_2, similar, net, mean_):

    h5_1_fid = h5py.File(h5_path_1, "r");
    h5_1_data = np.asarray(h5_1_fid['/data']);
    h5_1_label = np.asarray(h5_1_fid['/label']);
    h5_1_fid.close();

    h5_2_fid = h5py.File(h5_path_2, "r");
    h5_2_data = np.asarray(h5_2_fid['/data']);
    h5_2_label = np.asarray(h5_2_fid['/label']);
    h5_2_fid.close();

    h5_1_data_subtracted = np.zeros(h5_1_data.shape);
    for count in range(h5_1_data.shape[0]):
        h5_1_data_subtracted[count, :, :, :] = h5_1_data[count, :, :, :] - mean_;

    h5_2_data_subtracted = np.zeros(h5_2_data.shape);
    for count in range(h5_2_data.shape[0]):
        h5_2_data_subtracted[count, :, :, :] = h5_2_data[count, :, :, :] - mean_;

    net.blobs['data'].data[...] = h5_1_data_subtracted;
    out = net.forward()
    out_1 = np.copy(out['prob']) # do not referencig

    net.blobs['data'].data[...] = h5_2_data_subtracted;
    out = net.forward()
    out_2 = np.copy(out['prob']) # do not referencing

    diff = np.argmax(out_1, 1) - np.argmax(out_2, 1);

    if  (similar == 1): # similar
        indexes = np.where(diff == 0)[0];
    elif (similar == 0): # dissimilar
        indexes = np.where(diff != 0)[0];

    indexes_str = ','.join(str(index) for index in indexes);
    print ('%s %s %d:    %s' % (h5_path_1, h5_path_2, int(similar),indexes_str));

    return indexes



def main():
    check_argv(sys.argv);

    network = sys.argv[1];
    model = sys.argv[2];
    mean_file = sys.argv[3];

    pair_list = sys.argv[4];
    (patch_1_paths, patch_2_paths, similarities) = read_list(pair_list);

    output_file = sys.argv[5];

    net = caffe.Net(network, model, caffe.TEST)

    # mean = np.load(mean_file); # in case of npy

    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(  mean_file, 'rb' ).read();
    blob.ParseFromString(data)
    mean = np.array( caffe.io.blobproto_to_array(blob) );

    fid = open(output_file, 'w');

    for count in range(len(patch_1_paths)):

        # which sample did have same label
        sampling_indexes = check_pair(patch_1_paths[count], patch_2_paths[count], int(similarities[count]), net, mean);

        indexes_str = ','.join(str(sampling_index) for sampling_index in sampling_indexes);

        fid.write('%s,%s,%s \n' % (patch_1_paths[count], patch_2_paths[count], indexes_str));

    fid.close();

if __name__ == "__main__":
    main()
