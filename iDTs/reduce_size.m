function [ output_args ] = reduce_size( raw_file, reduced_file, pca_dict, reduce_size )

load(pca_dict);

feature_raw = importdata(raw_file, ',');

coeff_reduced = coeff(:,1:reduce_size);
feature_reduced = feature_raw * coeff_reduced;

csvwrite(reduced_file, feature_reduced);


end
