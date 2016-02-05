function [return_log] = sort_features(raw_file, sorted_file, verb_features_dir)
  % save(output, 'vids', 'opflows', 'feature_mats'); -> path of features file
  load(raw_file);

  load('verbs_list.mat');

  labels_list = cellstr(verbs_list);

  verbs_files = {};
  verbs_features = {};

  verbs_indexes = {};

  vids_labels = {};
  for index=1:size(vids, 1)

    vid = vids{index};
    vid_splitted = strsplit(vid, '/');
    vid_label = vid_splitted(end -1);
    vids_labels(index) = vid_label;

  end

  % loop through labels_list
  for index=1:size(labels_list, 1)
    label = labels_list{index};
    label_indexes = [];

    for count=1:size(vids_labels, 2)
      if (strcmp(label, vids_labels{count}))
        label_indexes = [label_indexes count];
      end
    end

    if (size(label_indexes, 2) > 0)
      verbs_indexes{index} = label_indexes;
    end

  end

  save(sorted_file, 'vids', 'opflows', 'feature_mats', 'verbs_indexes');

  % save each verb feature in  verb_features_dir

  for index=1:size(labels_list, 1)

    disp(labels_list{index});

    verb_features_file = sprintf('%s/%s', verb_features_dir, labels_list{index});
    verb_indexes = verbs_indexes{index};

    loader = load(feature_mats{verb_indexes(index)} );
    feature_tmp = loader.feature;

    h = size(verb_indexes, 2);
    w = size(feature_tmp, 2);

    verb_features = zeros([h  w]);

    for row=1:size(verb_indexes, 2)

      %disp(feature_mats{verb_indexes(row)});
      loader = load(feature_mats{verb_indexes(row)});
      feature_tmp = loader.feature;
      verb_features(row, :) = feature_tmp;

    end

    disp(verb_features_file);
    save(verb_features_file, 'vids', 'opflows', 'feature_mats', 'verb_indexes', 'verb_features');

  end

end