__author__ = 'gachiemchiep'

import sys, os, h5py, string, cv2
import numpy as np

# without mean file training will be hell
# when testing, subtracting mean file is key

def check_argv(argv_):
    if not (len(argv_) == 4):
        print "Usage python %s imgs_dir, output_hdf5" % (argv_[0])
        sys.exit(0);
    else:
        imgs_dir = argv_[1];
        if not (os.path.exists(imgs_dir) or os.access(imgs_dir, os.R_OK)):
            print "%s is not exist or unreadable" % (imgs_dir);
            sys.exit(0);

        output_hdf5 = argv_[2];
        if not (os.path.exists(os.path.dirname(output_hdf5)) and os.access(os.path.dirname(output_hdf5), os.W_OK)):
            print "%s parent dir is not exist or unreadable" % (imgs_dir, os.path.dirname(imgs_dir));
            sys.exit(0)

        option = argv_[3];
        if not option in ("crop", "noncrop", "noncrop_random"):
            print "%s is not available option" % (option);
            print "crop/noncrop";
            sys.exit(0)


def get_img_files(path_, key_):
    img_files_ = [];
    for img_file_ in os.listdir(path_):
        if key_ in img_file_:
            img_file_tmp_ = img_file_.replace("\n", "").replace("\r", "");
            img_files_.append(os.path.join(path_, img_file_tmp_));

    return (img_files_);


def merge_img_files_all(img_paths_, sampling_indexes_):

    img_1 = cv2.imread(img_paths_[0], cv2.COLOR_BAYER_BG2BGR);
    img_h = img_1.shape[0];
    img_w = img_1.shape[1];
    img_channels = img_1.shape[2];

    sampling_count = len(sampling_indexes_);
    blob_num = sampling_count;
    blob_channel = img_channels;
    blob_height = img_h;
    blob_width = img_w;

    img_files_merged = np.zeros([blob_num, blob_channel, blob_height, blob_width]);

    for index in range(sampling_count):  # 0 -> 24

        img_raw = cv2.imread(img_paths_[sampling_indexes_[index]], cv2.COLOR_BAYER_BG2BGR);
        img = np.zeros([img_channels, img_h, img_w]);

        # 0 1 2 -> 2 0 1
        # equal img = np.transpose(img, [2 0 1])
        for j in range(img_channels):
            img[j, :, :] = img_raw[:, :, j];

        img_files_merged[index, :, :, :] = img;

    return img_files_merged;


def merge_img_files(img_paths_, sampling_indexes_):
    img_1 = cv2.imread(img_paths_[0], cv2.COLOR_BAYER_BG2BGR);
    img_h = img_1.shape[0];
    img_w = img_1.shape[1];
    img_channels = img_1.shape[2];

    sampling_count = len(sampling_indexes_);
    blob_num = sampling_count * 5;
    blob_channel = img_channels;
    blob_height = 224;
    blob_width = 224;

    center_h_start = int((img_h - blob_height) / 2);
    center_h_end = center_h_start + blob_height;
    center_w_start = int((img_w - blob_width) / 2);
    center_w_end = center_w_start + blob_width;

    img_files_merged = np.zeros([blob_num, blob_channel, blob_height, blob_width]);

    for index in range(sampling_count):  # 0 -> 24

        img_raw = cv2.imread(img_paths_[sampling_indexes_[index]], cv2.COLOR_BAYER_BG2BGR);
        img = np.zeros([img_channels, img_h, img_w]);

        for j in range(img_channels):
            img[j, :, :] = img_raw[:, :, j];

        # normal
        top_left_index = (index * 5);
        top_right_index = (index * 5) + 1;
        center_index = (index * 5) + 2;
        bot_left_index = (index * 5) + 3;
        bot_right_index = (index * 5) + 4;

        img_files_merged[top_left_index, :, :, :] = img[:, 0:blob_height, 0:blob_width];
        img_files_merged[top_right_index, :, :, :] = img[:, 0:blob_height, (img_w - blob_width):img_w];
        img_files_merged[center_index, :, :, :] = img[:, center_h_start:center_h_end, center_w_start:center_w_end];
        img_files_merged[bot_left_index, :, :, :] = img[:, (img_h - blob_height):img_h, 0:blob_width];
        img_files_merged[bot_right_index, :, :, :] = img[:, (img_h - blob_height):img_h,
                                                     (img_w - blob_width):img_w];

        del img, img_raw;

    return img_files_merged;

# get the label
def get_label(OF_path_, sampling_indexes_, label_file_):
    labels_ = [];
    with open(label_file_, "r") as fid:
        for line in fid:
            label_ = line.replace('\n', '');
            labels_.append(label_);

    label_ids_ = np.zeros([len(sampling_indexes_) * 5, 1]);
    label_ids_[np.where(label_ids_ == 0)] = 255;

    OF_path_label_ = os.path.basename(OF_path_).split("_")[1];
    for count in range(len(labels_)):
        if (OF_path_label_ == labels_[count]):
            label_ids_[np.where(label_ids_ == 255)] = count;
            break;

    return label_ids_;

# get the label
def get_label_all(OF_path_, sampling_indexes_, label_file_):
    labels_ = [];
    with open(label_file_, "r") as fid:
        for line in fid:
            label_ = line.replace('\n', '');
            labels_.append(label_);

    label_ids_ = np.zeros([len(sampling_indexes_), 1]);
    label_ids_[np.where(label_ids_ == 0)] = 255;

    OF_path_label_ = os.path.basename(OF_path_).split("_")[1];
    for count in range(len(labels_)):
        if (OF_path_label_ == labels_[count]):
            label_ids_[np.where(label_ids_ == 255)] = count;
            break;

    return label_ids_;

def save_h5(h5_path_, data_, labels_):
    h5_fid = h5py.File(h5_path_, 'w');
    h5_fid.create_dataset('/data', dtype='uint8', data=data_, compression="gzip");
    h5_fid.create_dataset('/label', dtype='uint8', data=labels_, compression="gzip");
    h5_fid.close();


def main():
    check_argv(sys.argv);

    img_path = sys.argv[1];
    output_hdf5 = sys.argv[2];
    option = sys.argv[3];
    # key_x
    img_key = 'flow_i';

    img_paths = get_img_files(img_path, img_key);

    frame_count = len(img_paths);

    sampling_start = 3;
    sampling_dist = int((frame_count - 10 - 3) / 25);
    sampling_end = sampling_start + 25 * sampling_dist;

    sampling_indexes = [];
    for count in range(25):
        sampling_index = sampling_start + count * sampling_dist;
        sampling_indexes.append(sampling_index);

    if (option == "crop"):
        data = merge_img_files(img_paths, sampling_indexes);
        labels = get_label(img_path, sampling_indexes, 'UCF-101_labels.txt');
    elif (option =="noncrop"):
        data = merge_img_files_all(img_paths, sampling_indexes);
        labels = get_label_all(img_path, sampling_indexes, 'UCF-101_labels.txt');
    elif (option =="noncrop_random"):
        sampling_indexes2 = np.asarray(sampling_indexes);

        keys = np.random.permutation(len(sampling_indexes));
        print keys

        sampling_indexes = sampling_indexes2[keys[1:11]];

        print sampling_indexes2[keys[1:11]]

        data = merge_img_files_all(img_paths, sampling_indexes);

        print data.shape

        labels = get_label_all(img_path, sampling_indexes, 'UCF-101_labels.txt');


    save_h5(output_hdf5, data, labels);


if __name__ == "__main__":
    main()
