function [return_log] = merge_OFs(OFs_dir, stacked_count, output_hdf5)
% extension is : flow_i_0035.jpg, flow_x_0035.jpg, flow_y_0035.jpg
% number : frame_num
% flow_i: image
% flow_x: x part
% flow_y: y part

OFs_x_key = 'flow_x_*.jpg';
OFs_y_key = 'flow_y_*.jpg';

OFs_x_files = dir(fullfile(OFs_dir, OFs_x_key));
OFs_y_files = dir(fullfile(OFs_dir, OFs_y_key));

vid_frame_count = size(OFs_x_files, 1);

samples_count = 25; % 25 opflows
opflows_per_sample = 5; % 4 corners and center

h_resize = 256;
w_resize = 340;

sample_ids = floor(linspace(2, vid_frame_count - stacked_count - 1, samples_count));

stacked_cropped_opflows = zeros(w_resize, h_resize, stacked_count*2, samples_count*opflows_per_sample);


stop using matlab to generate hdf5 -? use the python script

h5_1_data[1, 1, :, :]
Out[10]:
array([[ 0.75720023,  0.75372909,  0.38044585,  0.56782164,  0.07585429],
       [ 0.05395012,  0.53079755,  0.77916723,  0.93401068,  0.12990621],
       [ 0.56882366,  0.46939064,  0.01190207,  0.33712264,  0.16218231],
       [ 0.79428454,  0.31121504,  0.52853314,  0.16564873,  0.60198194]])


>> a(:, :, 1, 1)

ans =

    0.2785    0.9706    0.4218    0.0357
    0.5469    0.9572    0.9157    0.8491
    0.9575    0.4854    0.7922    0.9340
    0.9649    0.8003    0.9595    0.6787
    0.1576    0.1419    0.6557    0.7577

>> a(:, :, 1, 1)'

ans =

    0.2785    0.5469    0.9575    0.9649    0.1576
    0.9706    0.9572    0.4854    0.8003    0.1419
    0.4218    0.9157    0.7922    0.9595    0.6557
    0.0357    0.8491    0.9340    0.6787    0.7577


data was totally messed up



make a python script and run on gp machine to merge OFs and etc


end