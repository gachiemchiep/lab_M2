function [return_log] = show_VisualRank(sorted_file, verbs_features_ranked_dir, output_text)
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

  fid = fopen(output_text, 'w');

  for row=1:size(verb_features_paths, 2)

    % print marker
    for count=1:10
      fprintf(fid, '#');
    end
    fprintf(fid, '\n');

    loader_row = load(verb_features_paths{row});
    vids_row = loader_row.vids;

    ranked_id_relative = loader_row.idx;
    ranked_id_absolute = loader_row.verb_indexes(ranked_id_relative);

    vids_row_ranked = vids_row(ranked_id_absolute, :);

    for count=1:size(vids_row_ranked, 1)
      fprintf(fid, '%s\n', vids_row_ranked{count});
    end

  end

  for count=1:10
      fprintf(fid, '#');
  end
  fclose(fid);

end