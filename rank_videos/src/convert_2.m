function [return_log] = convert(input_mat, output_mat)

  % features
  load(input_mat);
  feature_reshape = reshape(features',[1 numel(features)]);
  feature = feature_reshape / norm(feature_reshape); % L2 norm

% feature -> feature_old : feature_old = reshape(feature, [2048 125])'

  save(output_mat,'feature');
end