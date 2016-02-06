__author__ = 'gachiemchiep'

import sys, os, leveldb, cv2, h5py
import numpy as np

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe

caffe.set_device(1);
caffe.set_mode_gpu();


def check_argv(argv_):
    if not (len(argv_) == 5):
        print "Usage python %s network trained_model mean_file test_h5_list" % (argv_[0])
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


def read_test_h5_list(list_):
    files = [];
    with open(list_) as fid:
        for line in fid:
            line_new = line.replace('\n', '').replace('\r', '')
            files.append(line_new);

    return files

def main():

    check_argv(sys.argv);

    network = sys.argv[1];
    model = sys.argv[2];
    mean_file = sys.argv[3];
    test_h5_list = sys.argv[4];

    test_h5s = read_test_h5_list(test_h5_list);

    net = caffe.Net(network, model, caffe.TEST)

    blob = caffe.proto.caffe_pb2.BlobProto()
    data = open(  mean_file, 'rb' ).read()
    blob.ParseFromString(data)
    mean = np.array( caffe.io.blobproto_to_array(blob) )
    # mean = np.load(mean_file);

    accuracy_count = 0;
    samples_count = len(test_h5s);

    for index in range(len(test_h5s)):

        h5_fid = h5py.File(test_h5s[index], "r");
        h5_data = np.asarray(h5_fid['/data']);
        h5_label = np.asarray(h5_fid['/label']);
        h5_fid.close();

        h5_data_subtracted = np.zeros(h5_data.shape);

        for count in range(h5_data.shape[0]):
            h5_data_subtracted[count, :, :, :] = h5_data[count, :, :, :] - mean;

        net.blobs['data'].data[...] = h5_data_subtracted;
        out = net.forward()

        output_avg = np.sum(out['prob'], 0) / out['prob'].shape[0];
        print ('%s,  Label:  %d    Predict:  %d    Score:  %0.2f' % (
        test_h5s[index], h5_label[0], np.argmax(output_avg), output_avg[np.argmax(output_avg)]));

        if (h5_label[0] == np.argmax(output_avg)):
            accuracy_count = accuracy_count + 1;


    print('Samples_count:  %d  \t  Accuracy_count:  %d' % (samples_count, accuracy_count));

if __name__ == "__main__":
    main()

