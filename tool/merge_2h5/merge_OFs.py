__author__ = 'gachiemchiep'

import sys, os, h5py, string, cv2
import numpy as np

# Remeber : sampling 25x5 is more than enough -> why -> because i am lazy
# without mean file training will be hell
# when testing, subtracting mean file is key

OF_x_KEY = 'flow_x';
OF_y_KEY = 'flow_y';


def check_argv(argv_):
    if not (len(argv_) == 6):
        print "Usage python %s OFs_dir, stacked_count, output_hdf5, crop/noncrop sampling_count" % (argv_[0])
        sys.exit(0);
    else:
        OFs_dir = argv_[1];
        if not (os.path.exists(OFs_dir) or os.access(OFs_dir, os.R_OK)):
            print "%s is not exist or unreadable" % (OFs_dir);
            sys.exit(0);

        output_hdf5 = argv_[3];
        if not (os.path.exists(os.path.dirname(output_hdf5)) and os.access(os.path.dirname(output_hdf5), os.W_OK)):
            print "%s parent dir is not exist or unreadable" % (OFs_dir, os.path.dirname(OFs_dir));
            sys.exit(0)

        option = argv_[4];
        if not option in ("crop", "noncrop"):
            print "%s is not available option" % (option);
            print "crop/noncrop";
            sys.exit(0)

        sampling_count = int(argv_[5]);


def get_OF_files(path_, key_):
    OF_files_ = [];
    for OF_file_ in os.listdir(path_):
        if key_ in OF_file_:
            OF_file_tmp_ = OF_file_.replace("\n", "").replace("\r", "");
            OF_files_.append(os.path.join(path_, OF_file_tmp_));

    return (OF_files_);


# do not crop
def merge_OF_files_all(OF_x_paths_, OF_y_paths_, stacked_count_, sampling_indexes_):
    img_1 = cv2.imread(OF_x_paths_[0], cv2.IMREAD_GRAYSCALE);
    img_h = img_1.shape[0];
    img_w = img_1.shape[1];

    sampling_count = len(sampling_indexes_);  # 25
    blob_num = sampling_count;  # 25
    blob_channel = stacked_count_ * 2;
    blob_height = img_h;
    blob_width = img_w;

    center_h_start = int((img_h - blob_height) / 2);
    center_h_end = center_h_start + blob_height;
    center_w_start = int((img_w - blob_width) / 2);
    center_w_end = center_w_start + blob_width;

    OF_files_merged = np.zeros([blob_num, blob_channel, blob_height, blob_width]);

    for index in range(sampling_count):  # 0 -> 24
        sampling_start = sampling_indexes_[index];
        sampling_end = sampling_indexes_[index] + stacked_count_;

        stacked_OFs = np.zeros([blob_channel, img_h, img_w]);
        # stacked_OFs_flipped = np.zeros([blob_channel, img_h, img_w]);
        # print('#######################################################')
        # print index;
        for path_index in range(sampling_start, sampling_end):
            blob_channel_index = path_index - sampling_start;

            OF_x = cv2.imread(OF_x_paths_[path_index], cv2.IMREAD_GRAYSCALE);
            # OF_x_flipped = cv2.flip(OF_x, 1);

            OF_y = cv2.imread(OF_y_paths_[path_index], cv2.IMREAD_GRAYSCALE);
            # OF_y_flipped = cv2.flip(OF_y, 1);

            stacked_OFs[blob_channel_index * 2, :, :] = OF_x;
            stacked_OFs[blob_channel_index * 2 + 1, :, :] = OF_y;

        OF_files_merged[index, :, :, :] = stacked_OFs;

        del stacked_OFs, OF_x, OF_y;

    return OF_files_merged;


def merge_OF_files(OF_x_paths_, OF_y_paths_, stacked_count_, sampling_indexes_):
    img_1 = cv2.imread(OF_x_paths_[0], cv2.IMREAD_GRAYSCALE);
    img_h = img_1.shape[0];
    img_w = img_1.shape[1];

    sampling_count = len(sampling_indexes_);  # 25
    blob_num = sampling_count * 5;  # 125 +125
    # blob_num = sampling_count * 5 * 2;  # 125 +125
    blob_channel = stacked_count_ * 2;
    blob_height = 224;
    blob_width = 224;

    center_h_start = int((img_h - blob_height) / 2);
    center_h_end = center_h_start + blob_height;
    center_w_start = int((img_w - blob_width) / 2);
    center_w_end = center_w_start + blob_width;

    OF_files_merged = np.zeros([blob_num, blob_channel, blob_height, blob_width]);

    for index in range(sampling_count):  # 0 -> 24
        sampling_start = sampling_indexes_[index];
        sampling_end = sampling_indexes_[index] + stacked_count_;

        stacked_OFs = np.zeros([blob_channel, img_h, img_w]);
        # stacked_OFs_flipped = np.zeros([blob_channel, img_h, img_w]);
        # print('#######################################################')
        # print index;
        for path_index in range(sampling_start, sampling_end):
            blob_channel_index = path_index - sampling_start;

            OF_x = cv2.imread(OF_x_paths_[path_index], cv2.IMREAD_GRAYSCALE);
            # OF_x_flipped = cv2.flip(OF_x, 1);

            OF_y = cv2.imread(OF_y_paths_[path_index], cv2.IMREAD_GRAYSCALE);
            # OF_y_flipped = cv2.flip(OF_y, 1);

            stacked_OFs[blob_channel_index * 2, :, :] = OF_x;
            stacked_OFs[blob_channel_index * 2 + 1, :, :] = OF_y;

            # print('%s \t %s' % (OF_x_paths_[path_index], OF_y_paths_[path_index]));
            # print('%d \t %d' %(blob_channel_index * 2, blob_channel_index * 2 + 1));
            # stacked_OFs_flipped[blob_channel_index * 2, :, :] = OF_x_flipped;
            # stacked_OFs_flipped[blob_channel_index * 2 + 1, :, :] = OF_y_flipped;

        # normal
        top_left_index = (index * 5);
        top_right_index = (index * 5) + 1;
        center_index = (index * 5) + 2;
        bot_left_index = (index * 5) + 3;
        bot_right_index = (index * 5) + 4;

        # print('%d\t%d\t%d\t%d\t%d' %(top_left_index, top_right_index, center_index, bot_left_index, bot_right_index));

        OF_files_merged[top_left_index, :, :, :] = stacked_OFs[:, 0:blob_height, 0:blob_width];
        OF_files_merged[top_right_index, :, :, :] = stacked_OFs[:, 0:blob_height, (img_w - blob_width):img_w];
        OF_files_merged[center_index, :, :, :] = stacked_OFs[:, center_h_start:center_h_end,
                                                 center_w_start:center_w_end];
        OF_files_merged[bot_left_index, :, :, :] = stacked_OFs[:, (img_h - blob_height):img_h, 0:blob_width];
        OF_files_merged[bot_right_index, :, :, :] = stacked_OFs[:, (img_h - blob_height):img_h,
                                                    (img_w - blob_width):img_w];

        ### normal
        # top_left_index = (index * 10);
        # top_right_index = (index * 10) + 1;
        # center_index = (index * 10) + 2;
        # bot_left_index = (index * 10) + 3;
        # bot_right_index = (index * 10) + 4;
        #
        # OF_files_merged[top_left_index, :, :, :] = stacked_OFs[:, 0:blob_height, 0:blob_width];
        # OF_files_merged[top_right_index, :, :, :] = stacked_OFs[:, 0:blob_height, (img_w - blob_width):img_w];
        # OF_files_merged[center_index, :, :, :] = stacked_OFs[:, center_h_start:center_h_end, center_w_start:center_w_end];
        # OF_files_merged[bot_left_index, :, :, :] = stacked_OFs[:, (img_h - blob_height):img_h, 0:blob_width];
        # OF_files_merged[bot_right_index, :, :, :] = stacked_OFs[:, (img_h - blob_height):img_h,
        #                                             (img_w - blob_width):img_w];

        ####flipped
        # top_left_index = (index * 10) + 5;
        # top_right_index = (index * 10) + 6;
        # center_index = (index * 10) + 7;
        # bot_left_index = (index * 10) + 8;
        # bot_right_index = (index * 10) + 9;
        #
        # OF_files_merged[top_left_index, :, :, :] = stacked_OFs_flipped[:, 0:blob_height, 0:blob_width];
        # OF_files_merged[top_right_index, :, :, :] = stacked_OFs_flipped[:, 0:blob_height, (img_w - blob_width):img_w];
        # OF_files_merged[center_index, :, :, :] = stacked_OFs_flipped[:, center_h_start:center_h_end, center_w_start:center_w_end];
        # OF_files_merged[bot_left_index, :, :, :] = stacked_OFs_flipped[:, (img_h - blob_height):img_h, 0:blob_width];
        # OF_files_merged[bot_right_index, :, :, :] = stacked_OFs_flipped[:, (img_h - blob_height):img_h,
        #                                             (img_w - blob_width):img_w];

        del stacked_OFs, OF_x, OF_y;

    return OF_files_merged;


# get the label
def get_label(OF_path_, sampling_indexes_, label_file_):
    labels_ = [];
    with open(label_file_, "r") as fid:
        for line in fid:
            label_ = line.replace('\n', '');
            labels_.append(label_);

    label_ids_ = np.zeros([len(sampling_indexes_) * 5, 1]);
    label_ids_[np.where(label_ids_ == 0)] = 255;

    # print OF_path_;
    # print os.path.basename(OF_path_);
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

    # print OF_path_;
    # print os.path.basename(OF_path_);
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

    OF_path = sys.argv[1];
    stacked_count = int(sys.argv[2]);
    output_hdf5 = sys.argv[3];
    option = sys.argv[4];
    sampling_count = int(sys.argv[5]);

    OF_x_paths = get_OF_files(OF_path, OF_x_KEY);
    OF_y_paths = get_OF_files(OF_path, OF_y_KEY);

    frame_count = len(OF_x_paths);

    sampling_start = 3;
    sampling_dist = int(
        (frame_count - 10 - 3) / sampling_count);  # fixed sized, so only spatial can be used with 10opflows, 1opflows, 5opflows
    sampling_end = sampling_start + sampling_count * sampling_dist;

    sampling_indexes = [];
    for count in range(sampling_count):
        sampling_index = sampling_start + count * sampling_dist;
        sampling_indexes.append(sampling_index);

    if (option == "crop"):
        data = merge_OF_files(OF_x_paths, OF_y_paths, stacked_count, sampling_indexes);
        labels = get_label(OF_path, sampling_indexes, 'UCF-101_labels.txt');
    elif (option =="noncrop"):
        data = merge_OF_files_all(OF_x_paths, OF_y_paths, stacked_count, sampling_indexes);
        labels = get_label_all(OF_path, sampling_indexes, 'UCF-101_labels.txt');

    save_h5(output_hdf5, data, labels);


if __name__ == "__main__":
    main()
