__author__ = 'gachiemchiep'

import sys, os, cv2, h5py
import numpy as np
import scipy.io as sio

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe

caffe.set_device(1);
caffe.set_mode_gpu();


def check_argv(argv_):
    if not (len(argv_) == 6):
        print "Usage python %s network trained_model mean_file h5_list features_directory" % (argv_[0])
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

        h5_list = argv_[4];
        if not (os.path.exists(h5_list) or os.access(h5_list, os.R_OK)):
            print "test_h5_list:  %s is not exist or unreadable" % (h5_list);
            sys.exit(0);

        features_dir = argv_[5];
        if not (os.path.exists(h5_list) or os.access(features_dir, os.W_OK)):
            print "test_h5_list:  %s is not exist or unreadable" % (features_dir);
            sys.exit(0);


def read_h5_list(list_):
    h5_paths = [];
    with open(list_) as fid:
        for line in fid:
            line_new = line.replace('\n', '').replace('\r', '')
            h5_paths.append(line_new);

    return h5_paths


def main():
    check_argv(sys.argv);

    network = sys.argv[1];
    model = sys.argv[2];
    mean_file = sys.argv[3];
    h5_list = sys.argv[4];
    features_dir = sys.argv[5];

    # network = 'temporal_cls.txt';
    # model = 'temporal_v2.caffemodel';
    # mean_file = '10opflows_mean.binaryproto'
    # h5_list = 'test.txt'
    # features_dir = './'

    h5_paths = read_h5_list(h5_list);

    net = caffe.Net(network, model, caffe.TEST)

    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(  mean_file, 'rb' ).read()
    blob.ParseFromString(data)
    mean = np.array( caffe.io.blobproto_to_array(blob) );

    h5_path = h5_paths[1];

    h5_fid = h5py.File(h5_path, "r");
    h5_data = np.asarray(h5_fid['/data']);
    h5_fid.close();

    h5_data_mean = np.zeros([h5_data.shape[0], mean.shape[1], mean.shape[2], mean.shape[3]]);
    print h5_data_mean.shape;
    for count in range(h5_data.shape[0]):
        h5_data_mean[count, :, :, :] = mean;

    for index in range(len(h5_paths)):

        h5_path = h5_paths[index];

        h5_name = os.path.basename(h5_path).replace(".h5", ".mat");
        feature_path = os.path.join(features_dir, h5_name);

        if os.path.exists(feature_path):
            continue;

        print('%s %s' %(h5_path, feature_path));

        h5_fid = h5py.File(h5_path, "r");
        h5_data = np.asarray(h5_fid['/data']);
        h5_fid.close();

        net.blobs['data'].data[...] = h5_data - h5_data_mean;
        net.forward();
        features = net.blobs['fc7'].data.copy()

        #np.savetxt(feature_path, features, delimiter=",")
        sio.savemat(feature_path, {'features':features})



if __name__ == "__main__":
    main()



