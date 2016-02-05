function [return_log] = cal_trees_ranked_2(sorted_file, verbs_features_ranked_dir, output_img)
  % 'vids', 'opflows', 'features', 'verbs_indexes'
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

  % save(verb_features_file, 'vids', 'opflows', 'feature_mats', 'verb_indexes', 'verb_features');
  loader_row = load(verb_features_paths{1});

  features_row = loader_row.verb_features;

  verb_count = size(verb_features_paths, 2);
  feature_size = size(features_row, 2) * 125;

  verb_avg_features = zeros([verb_count feature_size]);

  % select [250 x 2048] -> 2 x 256000 -> avg

  disp(size(verb_features_paths));

  for row=1:size(verb_features_paths, 2)

    loader_row = load(verb_features_paths{row});
    features_row = loader_row.verb_features;

    % 125 x 2048
    features_row_ranked = features_row(loader_row.idx(1:125), :);

    % samples_count x 256000
    features_row_ranked_2 = reshape(features_row_ranked', [256000 1])';

    % mean values
    features_row_mean = mean(features_row_ranked_2);

    verb_avg_features(row, :) = features_row_mean;

  end

  output_img_avg_mat = strrep(output_img, '.fig', '_avg.mat');
  tree = linkage(verb_avg_features,'ward','euclidean');

  D = pdist(verb_avg_features);
  leafOrder = optimalleaforder(tree,D)

  D_square = squareform(D);
  verb_dists = D_square;
  save(output_img_avg_mat, 'verb_dists');


  % all
  output_img_avg = strrep(output_img, '.fig', '_all_avg.fig');
  output_img_avg_png = strrep(output_img, '.fig', '_all_avg.png');
  output_img_avg_eps = strrep(output_img, '.fig', '_all_avg.eps');

  draw = figure;

  H = dendrogram(tree, 0, 'Orientation','left','ColorThreshold','default', 'Labels', labels_list );
  set(H,'LineWidth',2);
  set(gca,'fontsize',14);

  savefig(draw, output_img_avg);
  saveas(draw, output_img_avg_eps);

  r = 500; % pixels per inch
  set(draw, 'PaperUnits', 'inches', 'PaperPosition', [0 0 27 19.2]);
  print(draw,'-dpng',sprintf('-r%d',r), output_img_avg_png);

  close(draw);

  % 0-100
  output_img_avg = strrep(output_img, '.fig', '_0-100_avg.fig');
  output_img_avg_png = strrep(output_img, '.fig', '_0-100_avg.png');
  output_img_avg_eps = strrep(output_img, '.fig', '_0-100_avg.eps');

  draw = figure;

  H = dendrogram(tree, 0, 'Orientation','left','ColorThreshold','default', 'Labels', labels_list );
  set(H,'LineWidth',2)
  set(gca,'XLim',[0 100]);
  set(gca,'fontsize',14);

  savefig(draw, output_img_avg);
  saveas(draw, output_img_avg_eps);

  r = 500; % pixels per inch
  set(draw, 'PaperUnits', 'inches', 'PaperPosition', [0 0 27 19.2]);
  print(draw,'-dpng',sprintf('-r%d',r), output_img_avg_png);

  close(draw);

  % 0-10
  output_img_avg = strrep(output_img, '.fig', '_0-10_avg.fig');
  output_img_avg_png = strrep(output_img, '.fig', '_0-10_avg.png');
  output_img_avg_eps = strrep(output_img, '.fig', '_0-10_avg.eps');

  draw = figure;

  H = dendrogram(tree, 0, 'Orientation','left','ColorThreshold','default', 'Labels', labels_list );
  set(H,'LineWidth',2)
  set(gca,'XLim',[0 10]);
  set(gca,'fontsize',14);

  savefig(draw, output_img_avg);
  saveas(draw, output_img_avg_eps);

  r = 500; % pixels per inch
  set(draw, 'PaperUnits', 'inches', 'PaperPosition', [0 0 27 19.2]);
  print(draw,'-dpng',sprintf('-r%d',r), output_img_avg_png);

  close(draw);

  % 0-1
  output_img_avg = strrep(output_img, '.fig', '_0-1_avg.fig');
  output_img_avg_png = strrep(output_img, '.fig', '_0-1_avg.png');
  output_img_avg_eps = strrep(output_img, '.fig', '_0-1_avg.eps');

  draw = figure;

  H = dendrogram(tree, 0, 'Orientation','left','ColorThreshold','default', 'Labels', labels_list );
  set(H,'LineWidth',2)
  set(gca,'XLim',[0 1]);
  set(gca,'fontsize',14);

  savefig(draw, output_img_avg);
  saveas(draw, output_img_avg_eps);

  r = 500; % pixels per inch
  set(draw, 'PaperUnits', 'inches', 'PaperPosition', [0 0 27 19.2]);
  print(draw,'-dpng',sprintf('-r%d',r), output_img_avg_png);

  close(draw);


end