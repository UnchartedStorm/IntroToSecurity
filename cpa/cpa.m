% Import data from in.mat
in = importdata('in.mat');
n = length(in);

% define the sbox used in PRESENT
% C 5 6 B 9 0 A D 3 E F 8 4 7 1 2
sbox = [12 5 6 11 9 0 10 13 3 14 15 8 4 7 1 2];
m = 16;

% Construct the value prediction matrix
% M = S[p_i xor 8-bit-number], row indexed by i

% Convert the matrix into the power-prediction matrix by using the Hamming
% weight model
pred = zeros(n, m);
for i = 1:n
    for j = 1:m
        x = sbox(bitxor(in(i), j-1) + 1);
        % disp(x)
        % hamming weight 
        pred(i, j) = sum(dec2bin(x).' == '1');
    end 
end

% disp(M)

traces = importdata('traces.mat');

% For all possible k candidates, compute the column-wise correlation between the traces matrix
% and the power-prediction matrix

rho = corr(pred, traces);
% disp(rho)
% rho has dimensions 16 by 6990

% sort these values while maintaining the index, [(val, row, col)]
p = 6990;
to_sort = zeros(times(m,p), 3);
for i = 1:times(m,p)
    j = floor((i-1)/p) + 1;
    k = i - p*(j - 1);
    to_sort(i, 1) = abs(rho(j, k));
    to_sort(i, 2) = j;
    to_sort(i, 3) = k;
end

% disable auto rescaling
format longG

% sorts according to first col, which is the corr
sorted = sortrows(to_sort, 'descend');
% disp(sorted(1:100, :));

% evaluate the largest value for each key
max_to_sort = zeros(m, 2);
for i = 1:m
    for j = 1:times(m,p)
        if (sorted(j, 2) == i)
            max_to_sort(i, 2) = sorted(j, 1);
            max_to_sort(i, 1) = i - 1;
            break
        end 
    end 
end

max_val = sortrows(max_to_sort, 2, 'descend');

disp("max_val")
% k-ranking: in descending order of correlation
% first element row correspond to key number
disp(max_val)

% Create the following graph: For every time sample, plot the absolute correlation value for every k
% candidate. Highlight the top candidate (e.g. using a different color). A similar graph is provided
% in the book "Power Analysis Attacks by S. Mangard et al.", page 126, figure 6.3.

% Create the following graph: Run the attack with 500, 1k, 2k 4k, 8k and 12k power traces and for
% every attack(i.e. every number of traces), rank the candidates from best to worst 
% (based on the absolute correlation value).
% Focus on the correct candidate, i.e. the one you recovered previously using 14900 traces. Plot
% the correct candidate’s ranking (e.g. 1st, 2nd etc.) for all these attacks.


















