% Import data from in.mat
in = importdata('in.mat');
% for debugging
disp(length(in));
disp(in(length(in) - 1))

% define the sbox used in PRESENT
% C	 5	6	B	9	0	A	D	3	E	F	8	4	7	1	2
sbox = [12 5 6 0 9 7 10 13 3 14 15 8 4 11 1 2];

% Construct the value prediction matrix