function [return_log] = merge_features(vids_list, opflows_list, feature_mats_list, output)

  vids = textread(vids_list, '%s', 'delimiter', '\n');
  opflows = textread(opflows_list, '%s', 'delimiter', '\n');

  feature_mats = textread(feature_mats_list, '%s', 'delimiter', '\n');

  %loader = load(feature_mats{1});
  %feature_tmp = loader.feature;

  %features_count = size(feature_mats, 1);
  %feature_width = size(feature_tmp, 2);

  %features = zeros([features_count feature_width]);

  %for index=1:features_count
  %  loader = load(feature_mats{index});
  %  feature_tmp = loader.feature;
  %  features(index, :) = feature_tmp;
  %end

  save(output, 'vids', 'opflows', 'feature_mats');

end