function [ output_args ] = cal_fisher_dtct( fv_raw, fv_dict )
%
% calculate dictionary for fisher encoding

run('/export/space2/vugia/vlfeat-0.9.20/toolbox/vl_setup');

data_raw = csvread(fv_raw);

data = transpose(data_raw);

clearvars data_raw;

numClusters = 256;

[means, covariances, priors] = vl_gmm(data, numClusters);

save(fv_dict, 'means', 'covariances', 'priors');

end
