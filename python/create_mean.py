__author__ = 'gachiemchiep'

import sys;
sys.path.append("/export/space2/vugia/caffe/python/")
import caffe
import numpy as np
from caffe.proto import caffe_pb2
from caffe.io import array_to_blobproto

OFs = ["10"];
height = 224;
width = 224;

for count in range(len(OFs)):

    OF = OFs[count];
    stacked_count = int(OF) * 2;

    mean = np.zeros((1, stacked_count, height, width));
    mean[np.where(mean == 0)] = 128;

    blob = array_to_blobproto(mean);

    mean_file = OF + "opflows_mean.binaryproto";
    with open(mean_file, 'wb') as fid:
        fid.write(blob.SerializeToString());

    arr = np.array( caffe.io.blobproto_to_array(blob) );
    mean_file = OF + "opflows_mean.npy";
    np.save(  mean_file , arr )


for count in range(len(OFs)):

    OF = OFs[count];
    stacked_count = int(OF) * 2 * 2;

    mean = np.zeros((1, stacked_count, height, width));
    mean[np.where(mean == 0)] = 128;

    blob = array_to_blobproto(mean);

    mean_file = OF + "opflows_mean_siamese.binaryproto";
    with open(mean_file, 'wb') as fid:
        fid.write(blob.SerializeToString());

    arr = np.array( caffe.io.blobproto_to_array(blob) );
    mean_file = OF + "opflows_mean_siamese.npy";
    np.save(  mean_file , arr )

# image
