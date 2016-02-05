function idx = VisualRank(S)
% output:
% idx: ranked index vector

% input:
% S: Similarity Matrix

d = 0.85; % damping factor
err = 1e-6; % acceptable error in calculation of VR
max_iter = 100; % maximum iteration

% normalize S
m = length(S);
c = sum(S);
S = S./repmat(c,m,1);

k = 0; % number of iteration
OR = zeros(m,1); % old rankings
NR = zeros(m,1); % new rankings

while k < max_iter
    k = k+1;

    NR = d*S*OR + (1-d)/m; % using uniform damping vector

    if isempty(find((NR-OR-err)>0,1))
        fprintf('VisualRank calculation done. Number of iteration = %d',k);
        break;
    end

    OR = NR;

end

[~,idx] = sort(NR,'descend');

end
