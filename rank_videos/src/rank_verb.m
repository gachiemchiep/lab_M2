function [return_val] = rank_verb(verb_mat, verb_mat_rank)

% feature_mats, verb_features, verb_indexes, vids
load(verb_mat);

dists = pdist(verb_features);

dists_square = squareform(dists);

idx = VisualRank(dists_square);

verb_indexes_ranked = verb_indexes(idx);

save(verb_mat_rank, 'feature_mats', 'verb_features', 'verb_indexes', 'vids', 'idx');

end