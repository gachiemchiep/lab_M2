function [return_log] = combine_ST(spatial_mat, temporal_mat, output_mat)

% spatial_mat, temporal_mat : 1x256000 : feature
loader_S = load(spatial_mat);
loader_T = load(temporal_mat);

feature_S = loader_S.feature;
feature_T = loader_T.feature;

feature_ST = (feature_S + 2*feature_T) / 3;

feature = feature_ST;

% save as feature so it can work with old code
save(output_mat, 'feature');

end