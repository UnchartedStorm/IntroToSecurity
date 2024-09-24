% Differential Cryptanalysis on CipherTwo
clear all;
close all;

% generate plaintexts with differential equal to 0xf
no_pairs = 400;
m0 = randi(16, no_pairs, 1) - 1;
m1 = bitxor(m0, 15);

% initialize to zero the key guess counter
key_counter = zeros(1, 16);

% for all plaintext pairs
for i=1:no_pairs
    
    % compute the respective ciphertext pairs
    c0 = cipher_two(m0(i));
    c1 = cipher_two(m1(i));
    
    % delta_m = m0 xor m1 = delta_u = u0 xor u1 
    % we also know that delta_m = 0xf (since m is chosen that way)
    delta_m = 15;
    delta_u = delta_m;
    
    % from the difference distribution of the sbox we also know that when 
    % delta_u=0xf, then delta_v is likely to be 0xd (with probability
    % 10/16)
    
    % for all key guesses of key k2
    for key_guess = 0:15
       
        % invert the 3rd addroundkey
        x0 = bitxor(key_guess, c0);
        x1 = bitxor(key_guess, c1);
        
        % invert the sbox
        w0 = inv_sbox(x0);
        w1 = inv_sbox(x1);
        
        % compute the differential delta_w
        delta_w = bitxor(w0, w1);
        
        % we know that delta_w is equal to delta_v 
        delta_v = delta_w;
        
        % check if delta_v is equal to the highly likely difference 0xd and
        % if so increase the key guess counter
        if delta_v == 13
            key_counter(key_guess+1) = key_counter(key_guess+1) + 1;
        end
    
    end

    
end


% find which key guess has the largest counter
[max_val, max_index] = max(key_counter);

% the resulting key is stored in k2_recovered
k2_recovered = max_index - 1;

% compare it to the true key k2=3
k2_recovered == 3;

% visualize with a bar plot the counters for the k2 key guesses
bar(0:15, key_counter)

% using the recovered k2 we can also work backwards and recover k1 and k0
