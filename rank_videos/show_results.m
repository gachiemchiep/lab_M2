
%dist_file='UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';
%dist_file='../UCF-101_10opflows/UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';
%dist_file='UCF-101_ST/UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';


%dist_file='UCF-101_imgs/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';
%dist_file='UCF-101_10opflows/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';
%dist_file='UCF-101_ST/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';



%dist_file='UCF-101_imgs_siamese/UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';
%dist_file='UCF-101_10opflows_siamese/UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';
%dist_file='UCF-101_ST_siamese/UCF-101_vids_fc7_sorted_ranked_1.0_avg.mat';



dist_file='UCF-101_imgs_siamese/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';
%dist_file='UCF-101_10opflows_siamese/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';
%dist_file='UCF-101_ST_siamese/UCF-101_vids_fc7_sorted_ranked_0.5_avg.mat';

addpath('src/')
load('src/verbs_list.mat') ;

load(dist_file);
dists_vector = squareform(verb_dists, 'tovector');

[dists_vector_sorted, idx] = sort(dists_vector);
% first 101 is

min_dist = min(dists_vector);

max_count = 20;
for count=1:max_count

  [row, col] = find_id(idx(count),  size(verb_dists, 1));
  [row_2, col_2] = find_id(idx(count + max_count),  size(verb_dists, 1));

  %fprintf(1,'%d & %s & %s & %0.4f & %0.2f \\\\ \\hline \n', count,verbs_list{row}, verbs_list{col}, dists_vector(idx(count)),  dists_vector(idx(count))/min_dist );
  fprintf(1,'%d & %s & %s & %0.2e & %0.2f \\\\ \\hline \n', count,verbs_list{row}, verbs_list{col}, dists_vector(idx(count)),  dists_vector(idx(count))/min_dist );

end

clear


% asdhaksjdhakjshdkj

function [row, col] = find_id(val, square_size)

for count=2:square_size

  if (sum(linspace(1, count-1, count-1)) > val)
    row = count;
    col = val - sum(linspace(1, count-2, count-2));
    break;
  end

  if (sum(linspace(1, count-1, count-1)) == val)
    row = count;
    col = row - 1;
    break;
  end

end

end