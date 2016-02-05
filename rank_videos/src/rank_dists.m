function [return_log] = rank_dists(merge_dists_file, top_count, output_txt)
  % 'vids', 'oflows', 'dists'
  load(merge_dists_file);

  fid = fopen(output_txt, 'a');

  for index=1:size(dists, 1)
    dist = dists(index, :);
    [dist_sorted, idx] = sort(dist);

    vid_base = vids{index};

    vids_top = vids(idx(1:(top_count)));
    dist_top = dist(idx(1:(top_count)));

    fprintf(fid, '%s:%d,', vid_base, 0);

    for j=1:size(vids_top, 1)
      if (j == size(vids_top, 1))
        fprintf(fid, '%s:%f', vids_top{j}, dist_top(j));
      else
        fprintf(fid, '%s:%f,', vids_top{j}, dist_top(j));
      end
    end

    fprintf(fid, '\n');

  end

  fclose(fid);

  dis_txt = strrep(output_txt, '.txt', '_dis.txt');

  fid = fopen(dis_txt, 'a');

  for index=1:size(dists, 1)
    dist = dists(index, :);
    [dist_sorted, idx] = sort(dist, 'descend');

    vid_base = vids{index};

    vids_top = vids(idx(1:(top_count)));
    dist_top = dist(idx(1:(top_count)));

    fprintf(fid, '%s:%d,', vid_base, 0);

    for j=1:size(vids_top, 1)
      if (j == size(vids_top, 1))
        fprintf(fid, '%s:%f', vids_top{j}, dist_top(j));
      else
        fprintf(fid, '%s:%f,', vids_top{j}, dist_top(j));
      end
    end

    fprintf(fid, '\n');

  end

  fclose(fid);

end