function [ output_args ] = cal_pca( pca_raw, pca_dict )

% calculate pca dictionary
% some bug happen in csvread and dlread
% use importdata instead

data_raw = importdata(pca_raw, ',');

coeff = pca(data_raw);

save(pca_dict, 'coeff');

end
