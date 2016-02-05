function [return_log] = cal_trees(sorted_file, verbs_features_ranked_dir, output_img, selected_per)
  % 'vids', 'opflows', 'features', 'verbs_indexes'

  %sorted_file = '/host/space2/vugia/rank_videos/UCF-101_imgs/UCF-101_vids_fc7_sorted.mat'
  %verbs_features_ranked_dir = '/export/space/vugia/tmp/rank_videos/UCF-101_imgs/verb_features_ranked'
  %selected_per = 0.3

  load(sorted_file);

  load('verbs_list.mat');

  labels_list = cellstr(verbs_list);

  search_path = sprintf('%s/%s', verbs_features_ranked_dir, '*_ranked.mat');
  verb_features_files = dir(search_path);

  verb_features_paths = {};
  for index=1:size(verb_features_files, 1)

    verb_features_path = sprintf('%s/%s', verbs_features_ranked_dir, verb_features_files(index).name);
    verb_features_paths{index} = verb_features_path;

  end

  loader_row = load(verb_features_paths{1});
  features_row = loader_row.verb_features;
  features_row_mean = mean(features_row);

  sample_count = size(verb_features_paths, 2);
  feature_size = size(features_row_mean, 2);

  verb_avg_features = zeros([sample_count feature_size]);

  clearvars loader_row;

  for row=1:size(verb_features_paths, 2)

    disp(verb_features_paths{row});
    loader_row = load(verb_features_paths{row});
    features_row = loader_row.verb_features;

    sample_count = floor(size(features_row, 1) * selected_per);

    features_row_ranked = features_row(loader_row.idx(1:sample_count), :);
    disp(size(features_row_ranked));

    features_row_mean = mean(features_row_ranked);

    verb_avg_features(row, :) = features_row_mean;

    clearvars loader_row features_row_ranked;

  end

  disp(size(verb_avg_features));

  output_img_avg_mat = strrep(output_img, '.fig', '_avg.mat');
  tree = linkage(verb_avg_features,'ward','euclidean');

  %D_squareform = zeros(size(verb_features_paths, 2), size(verb_features_paths, 2));
  %for row=2:size(verb_features_paths, 2)
  %  for col=1:(row-1)
  %    dist = norm(verb_avg_features(row, :) - verb_avg_features(col, :));
  %    D_squareform(row, col) = dist;
  %    D_squareform(col, row) = dist;
  %  end
  %end
  %D = squareform(D_squareform, 'tovector');

  D = pdist(verb_avg_features);
  leafOrder = optimalleaforder(tree,D)

  D_square = squareform(D);
  verb_dists = D_square;
  save(output_img_avg_mat, 'verb_dists');

  % all
  output_img_avg = strrep(output_img, '.fig', '_all_avg.fig');
  output_img_avg_png = strrep(output_img, '.fig', '_all_avg.jpg');
  output_img_avg_eps = strrep(output_img, '.fig', '_all_avg.eps');

  draw = figure;

  H = dendrogram(tree, 0, 'Orientation','left','ColorThreshold','default', 'Labels', labels_list );
  set(H,'LineWidth',2)
  set(gca,'fontsize',14);

  savefig(draw, output_img_avg);
  saveas(draw, output_img_avg_eps);

  r = 0; % pixels per inch
  set(draw, 'PaperUnits', 'inches', 'PaperPosition', [0 0 27 19.2]);
  print(draw,'-djpg',sprintf('-r%d',r), output_img_avg_png);

  close(draw);




end