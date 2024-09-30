% Differential Cryptanalysis on CipherFour
clear all;
close all;


% Generate a few thousand 16-bit plaintexts pairs
% Each plaintext can be organized as 4 nibbles: [a b c d] 
% Note that a nibble is a 4-bit value
% Ensure that the difference between every plaintext pair (m0,m1) is 
% equal to (0 0 2 0)
no_pairs = 3000;
na = randi(16, no_pairs, 1) - 1;
nb = randi(16, no_pairs, 1) - 1;
nc = randi(16, no_pairs, 1) - 1;
nd = randi(16, no_pairs, 1) - 1;
ncd = bitxor(nc, 2);

stored_c0 = [];
stored_c1 = [];
size = 0;

% for all generated plaintext pairs 
for i=1:no_pairs
    
    % compute the respective ciphertext pairs using the cipher_four()
    % implementation
    c0 = cipher_four([na(i), nb(i), nc(i), nd(i)]);
    c1 = cipher_four([na(i), nb(i), ncd(i), nd(i)]);
    
    % apply filtering to the ciphertext pairs i.e. 
    % -compute the difference between the ciphertext pairs
    delta_c = bitxor(c0, c1);

    % -check if this difference could be originating from a correct pair
    % the correct pairs are: (0 0 h 0) where h is in {1,2,9,10} 
    check_1 = delta_c == [0, 0, 1, 0];
    check_2 = delta_c == [0, 0, 2, 0];
    check_3 = delta_c == [0, 0, 9, 0];
    check_4 = delta_c == [0, 0, 10, 0];

    % -if the ciphertext pair passes the filter's check, we keep it
    % otherwise, we discard it
    if check_1 | check_2 | check_3 | check_4
        stored_c0 = [stored_c0; c0];  % Append c0 as a row
        stored_c1 = [stored_c1; c1];  % Append c1 as a row
        size = size + 1;
    end
    
% end
end

disp(size)

% focus on the 3rd nibble of the ciphertext pairs that were kept after
% filtering

% initalize the counter for all key candidates to zero
key_counter = zeros(1, 16);

% for all ciphertexts that remain after filtering
for i=1:length(stored_c0)

    % for all key guesses of the 3rd nible of roundkey k6 
    for key_guess = 0:15
    
        % invert the 6th addkey operation
        x0 = bitxor(key_guess, stored_c0(i));
        x1 = bitxor(key_guess, stored_c1(i));

        % invert the sbox
        q0 = inv_sbox(x0);
        q1 = inv_sbox(x1);
        
        % compute the difference delta
        delta_q = bitxor(q0, q1);

        % compare the delta with the difference (0 0 2 0)
        % if they are equal then increment the the respective key counter
        % by one
        if delta_q == [0, 0, 2, 0]
            key_counter(key_guess + 1) = key_counter(key_guess + 1) + 1;
        end
    end
end

% find which key guess has the largest counter
disp(key_counter)
[max_val, max_index] = max(key_counter);
k6_recovered = max_index - 1;

% print and store the recovered key nibble
% you can also confirm by comparing it to the correct key nibble in
% cipher_four()
x = (k6_recovered == 12);
disp('x:')
disp(x)

% visualize with a bar plot the counters for the k6 key guesses
bar(0:15, key_counter);

