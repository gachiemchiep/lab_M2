function [return_log] = convert(input_txt, output_mat)
  feature_old = csvread(input_txt);
  %feature = reshape(feature_old,[1 numel(feature_old)]);  -> very  wrong

  feature_reshape = reshape(feature_old',[1 numel(feature_old)]);  % correct one
  feature = feature_reshape / norm(feature_reshape); % L2 norm

% feature -> feature_old : feature_old = reshape(feature, [2048 125])'

  save(output_mat,'feature');
end