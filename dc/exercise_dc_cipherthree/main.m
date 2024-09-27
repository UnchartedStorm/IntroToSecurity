% Differential Cryptanalysis on CipherThree
clear all;
close all;

% generate plaintexts with difference equal to 0xf
no_pairs = 1000;
m0 = randi(16, no_pairs, 1) - 1;
m1 = bitxor(m0, 15);

% initialize to zero the key guess counter
key_counter = zeros(1, 16);

% for all plaintext pairs
for i=1:no_pairs

    % compute the respective ciphertext pairs using cipher_three()
    c0 = cipher_three(m0(i));
    c1 = cipher_three(m1(i));

    % delta_m = m0 xor m1 = 0xf
    delta_m = 15;

    % we know that delta_u is equal to delta_m
    delta_u = delta_m;

    % from the difference distribution of the sbox we also know that when
    % delta_u=0xf, then delta_v is likely to be 0xd with probability 10/16

    % we know that delta_w is equal to delta_v

    % from the difference distribution of the sbox we also know that when
    % delta_w=0xd, then delta_x is likely to be 0xc with probability 6/16

    % we know that delta_y is equal to delta_x
    % Since delta_x is 0xc
    delta_y = 12;

    % assuming independent rounds compute the probability for the
    % differential characteristic 0xf -> 0xd -> 0xc


    % for all key guesses of key k3
    for key_guess = 0:15

        % invert the 4th addkey operation
        x0 = bitxor(key_guess, c0);
        x1 = bitxor(key_guess, c1);
        % invert the sbox
        y0 = inv_sbox(x0);
        y1 = inv_sbox(x1);

        % compute the differential delta_y under the key hypothesis
        delta_y_r = bitxor(y0, y1);

        % check if delta_y's match
        if delta_y_r == delta_y
           key_counter(key_guess + 1) = key_counter(key_guess + 1) + 1;
        end
    end
end

% recover the key k3 by finding which key guess has the largest counter
[max_val, max_index] = max(key_counter);
k3_recovered = max_index - 1;
% compare it to the true k3 key specified in cipher_three()
x = (k3_recovered == 7);
disp('x:')
disp(x)
% visualize with a bar plot the counters for the k3 key guesses
bar(0:15, key_counter);
