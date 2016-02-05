function [return_val] = marge_results_nn(unshuffled_list,fc_file,fc_p_file,output)

% unshuffled list: OF_h5_1,OF_h2_2,sim(1/0)
% fc_file       : siamese output
% fc_p_file     : siamese output
% output        : save file

[fc_files, fc_p_files, similarities] = textread(unshuffled_list, '%s %s %d', 'delimiter', ',');

fc_features = csvread(fc_file);
fc_p_features = csvread(fc_p_file);

features = [fc_features fc_p_features];
clearvars fc_features fc_p_features;



%%%%%%%%%%%%%%%%%%%%%%%%%%%
save(output, 'fc_files','fc_p_files','similarities','features','-v7.3');

end
