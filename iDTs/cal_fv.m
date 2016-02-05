function [ output_args ] = cal_fv( pca_feature, output_fv, fv_dict  )

run('/export/space2/vugia/vlfeat-0.9.17/toolbox/vl_setup');

load(fv_dict);

% feature = csvread(feature_file);
feature = importdata(pca_feature, ',');

% transform [index, dimension] -> [dimension, index]
feature_transposed = transpose(feature);

fv = vl_fisher(feature_transposed, means, covariances, priors, 'Fast');
disp(size(fv));
fv_transposed = transpose(fv);
fv = fv_transposed;


nan_count = sum(isnan(fv));

if (nan_count  > 0)
  exit
end

inf_count = sum(isinf(fv));
if (inf_count > 0)
  exit
end

save(output_fv, 'fv');

end
