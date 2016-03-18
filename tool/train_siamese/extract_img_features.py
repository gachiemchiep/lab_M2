__author__ = 'gachiemchiep'

import sys, os, cv2
import numpy as np
import scipy.io as sio

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe

caffe.set_device(1);
caffe.set_mode_gpu();


def check_argv(argv_):
    if not (len(argv_) == 6):
        print "Usage python %s network trained_model mean_file imgs_list features_file" % (argv_[0])
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

        imgs_list = argv_[4];
        if not (os.path.exists(imgs_list) or os.access(imgs_list, os.R_OK)):
            print "test_h5_list:  %s is not exist or unreadable" % (imgs_list);
            sys.exit(0);

        features_file = argv_[5];
        if os.path.exists(features_file):
            print "%s is exist" % (features_file);
            sys.exit(0);


def read_imgs_list(list_):
    paths_ = [];
    with open(list_) as fid:
        for line in fid:
            line_new = line.replace('\n', '').replace('\r', '')
            paths_.append(line_new);

    return paths_


def main():
    check_argv(sys.argv);

    network = sys.argv[1];
    model = sys.argv[2];
    mean_file = sys.argv[3];
    imgs_list = sys.argv[4];
    features_file = sys.argv[5];

    paths = read_imgs_list(imgs_list);

    net = caffe.Net(network, model, caffe.TEST)

    # mean file is saved as binaryproto
    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(  mean_file, 'rb' ).read()
    blob.ParseFromString(data)
    mean = np.array( caffe.io.blobproto_to_array(blob) );

    features = np.zeros([len(paths), 1024]);

    for index in range(len(paths)):

        path = paths[index];
        img_raw = cv2.imread(path);
        # Caltech
        img = cv2.resize(img_raw, (227, 227))
        img_data = np.transpose(img, [2, 0, 1]);  # h x w x channel -> channel x h x w

        net.blobs['data'].data[...] = img_data #- mean;
        net.forward();
        feature = net.blobs['fc7'].data.copy();
        print feature;
        features[index, :] = feature;

    sio.savemat(features_file, {'features':features});

if __name__ == "__main__":
    main()



