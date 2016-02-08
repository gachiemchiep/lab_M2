__author__ = 'gachiemchiep'

import numpy as np
import matplotlib.pyplot as plt

# Make sure that caffe is on the python path:
caffe_root = '/export/space2/vugia/caffe/python/'  # this file is expected to be in {caffe_root}/examples
import sys
sys.path.insert(0, caffe_root + 'python')

sys.path.append("/export/space2/vugia/caffe/python/")
import caffe
import caffe.imagenet

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

net = caffe.imagenet.ImageNetClassifier(caffe_root + 'examples/imagenet/imagenet_deploy.prototxt',
                                        caffe_root + 'examples/imagenet/caffe_reference_imagenet_model')
net.caffenet.set_phase_test()
net.caffenet.set_mode_gpu()

scores = net.predict(caffe_root + 'examples/images/cat.jpg')

