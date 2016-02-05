function [return_log] = cal_dists(features_file, output_file, start_index)
% divide into smaller part and run on cluster machines
% 'vids', 'opflows', 'feature_mats'

  loader = load(features_file);
  feature_mats = loader.feature_mats;

  dists = zeros([size(feature_mats, 1) size(feature_mats, 1)]);

  for row=start_index:start_index
    % load row th feature
    loader_row = load(feature_mats{row});
    feature_row = loader_row.feature;

    for col=1:(row-1)

      % load j th feature
      loader_col = load(feature_mats{col});
      feature_col = loader_col.feature;

      dist = sqrt(sum( (feature_row - feature_col) .^ 2) );

      dists(row, col) = dist;
      dists(col, row) = dist;

    end
  end

  save(output_file, 'dists');

end

