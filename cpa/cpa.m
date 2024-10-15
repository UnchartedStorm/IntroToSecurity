% Import data from in.mat
in = importdata('in.mat');
% for debugging
n = length(in);
disp(n)
disp(in(n))

% define the sbox used in PRESENT
% C	 5	6	B	9	0	A	D	3	E	F	8	4	7	1	2
sbox = [12 5 6 11 9 0 10 13 3 14 15 8 4 7 1 2];
m = 16;

% Construct the value prediction matrix
% M = S[p_i xor 8-bit-number], row indexed by i
M = zeros(n, m);
for i = 1:n
    for j = 1:m
        M(i, j) = sbox(bitxor(in(i), j));
    end 
end



