function [return_log] = merge_dists(vids_list, opflows_list, dists_list, output)

  vids = textread(vids_list, '%s', 'delimiter', '\n');
  opflows = textread(opflows_list, '%s', 'delimiter', '\n');

  dists_mats = textread(dists_list, '%s', 'delimiter', '\n');

  loader = load(dists_mats{1});
  dists_tmp = loader.dists;

  dists = zeros(size(dists_tmp));

  for index=1:size(dists_tmp, 1)
    loader = load(dists_mats{index});
    dists_tmp = loader.dists;

    dists = dists + dists_tmp;
  end

  save(output, 'vids', 'opflows', 'dists');

end