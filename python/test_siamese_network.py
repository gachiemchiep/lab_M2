__author__ = 'gachiemchiep'

import sys, os, leveldb, cv2, h5py
import numpy as np

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe

caffe.set_device(1);
caffe.set_mode_gpu();

########### input a pair then output the distances  ####

THRESHOLD = 1;


def check_argv(argv_):
    if not (len(argv_) == 5):
        print "Usage python %s network trained_model mean_file test_h5_pair_list" % (argv_[0])
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
    pairs = [];
    with open(list_) as fid:
        for line in fid:
            line_new = line.replace('\n', '').replace('\r', '')
            pairs.append(line_new);

    return pairs


def main():
    check_argv(sys.argv);

    network = sys.argv[1];
    model = sys.argv[2];
    mean_file = sys.argv[3];
    test_h5_list = sys.argv[4];

    test_h5_pairs = read_test_h5_list(test_h5_list);

    # network = 'NET/siamese_deploy.txt'
    # mean_file = '10opflows_mean.npy'
    # model = 'UCF-101_10opflows_siamese_3200_iter_75000.caffemodel'
    # test_h5_list = 'UCF-101_10opflows_train_3200.txt'

    net = caffe.Net(network, model, caffe.TEST)

    mean = np.load(mean_file);

    accuracy_count = 0;
    samples_count = len(test_h5_pairs);

    for index in range(len(test_h5_pairs)):

        pair = test_h5_pairs[index];

        h5_1 = pair.split(',')[0];
        h5_2 = pair.split(',')[1];
        label = pair.split(',')[2];

        h5_1_fid = h5py.File(h5_1, "r");
        h5_1_data = np.asarray(h5_1_fid['/data']);
        h5_1_fid.close();

        h5_2_fid = h5py.File(h5_2, "r");
        h5_2_data = np.asarray(h5_2_fid['/data']);
        h5_2_fid.close();

        h5_1_data_subtracted = np.zeros(h5_1_data.shape);
        h5_2_data_subtracted = np.zeros(h5_2_data.shape);

        dist_sum = 0;

        for count in range(h5_1_data.shape[0]):
            h5_1_data_subtracted[count, :, :, :] = h5_1_data[count, :, :, :] - mean;
            h5_2_data_subtracted[count, :, :, :] = h5_2_data[count, :, :, :] - mean;

            net.blobs['data'].data[...] = h5_1_data[count, :, :, :] - mean;
            net.blobs['data_p'].data[...] = h5_2_data[count, :, :, :] - mean;

            out = net.forward();

            dist = np.linalg.norm(out['fc7'] - out['fc7_p']);
            dist_sum = dist_sum + dist;

            sys.stdout.write('%0.2f ' % (dist));

        print '';

        dist_avg = dist_sum / h5_1_data.shape[0];

        print('%s \t %s \t %s \t %f ' % (h5_1, h5_2, label, dist_avg));


if __name__ == "__main__":
    main()


# net = caffe.Net('two_stream_temporal_deploy.prototxt',
#                 'two_stream_temporal_sp1.caffemodel',
#                 caffe.TEST)

# blob = caffe.proto.caffe_pb2.BlobProto()
# data = open(  'ucf_sof10L_mean_sp1.binaryproto' , 'rb' ).read()
# blob.ParseFromString(data)
# arr = np.array( caffe.io.blobproto_to_array(blob) )
# out = arr[0]
# np.save(  'ucf_sof10L_mean_sp1.npy' , out )


# load input and configure preprocessing
# transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
# transformer.set_mean('data', np.load('ucf_sof10L_mean_sp1.npy').mean(1).mean(1)); # should be in npy
# net = caffe.Net('temporal_cls.txt',
#                 'temporal_v2.caffemodel',
#                 caffe.TEST)
# mean = np.load('10opflows_mean.npy');
#
# # load the image in the data layer
#
# files = [];
# with open('test.txt') as fid:
#     for line in fid:
#         line_new = line.replace('\n', '').replace('\r', '')
#         files.append(line_new);
#
# accuracy_count = 0;
# samples_count = len(files);
#
# for index in range(len(files)):
#
#     h5_fid = h5py.File(files[index], "r");
#     h5_data = np.asarray(h5_fid['/data']);
#     h5_label = np.asarray(h5_fid['/label']);
#     h5_fid.close();
#
#     h5_data_subtracted = np.zeros(h5_data.shape);
#
#     for count in range(h5_data.shape[0]):
#         h5_data_subtracted[count, :, :, :] = h5_data[count, :, :, :] - mean;
#
#     net.blobs['data'].data[...] = h5_data_subtracted;
#     out = net.forward()
#
#     # for i in range(125):
#     #     net.blobs['data'].data[...] =  h5_data[i, :, :, :] ;#[range(1, 41), :, :, :];
#     #     #compute
#     #     out = net.forward()
#     #     print("Predicted class is #{}.".format(out['prob'].argmax()))
#
#     # other possibility : out = net.forward_all(data=np.asarray([transformer.preprocess('data', im)]))
#
#     # predict = [];
#
#     # predicted predicted class
#     # for i in range(h5_data.shape[0]):
#     #     predict.append(out['prob'][i].argmax());
#
#     # print(', '.join(map(str, predict)));
#
#     # predict_unique = np.unique(predict);
#     # count = [];
#     # for i in range(len(predict_unique)):
#     #     count.append(predict.count(predict_unique[i]));
#
#     # print ('%s, %d, %d, %d' % (files[index],  predict_unique[np.argmax(count)], np.max(count), h5_data.shape[0]));
#
#     output_avg = np.sum(out['prob'], 0) / out['prob'].shape[0];
#     print ('%s,  Label:  %d    Predict:  %d    Score:  %0.2f' % (
#     files[index], h5_label[0], np.argmax(output_avg), output_avg[np.argmax(output_avg)]));
#
#     if (h5_label[0] == np.argmax(output_avg)):
#         accuracy_count = accuracy_count + 1;
#
# print('Samples_count:  %d  \t  Accuracy_count:  %d' % (samples_count, accuracy_count));
