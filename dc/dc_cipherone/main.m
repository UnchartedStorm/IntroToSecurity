% Differential Cryptanalysis on CipherOne
clear all;
close all;

% generate plaintexts with differential equal to 0xf
no_pairs = 100;
m0 = randi(16, no_pairs, 1) - 1;
m1 = bitxor(m0, 15);

% initially we set all keys as possible for roundkey k1
k1_recovered = 0:15;

% for all plaintext pairs
for i=1:no_pairs
    
    % compute the respective ciphertext pairs
    c0(i) = cipher_one(m0(i));
    c1(i) = cipher_one(m1(i));
    
    % m0 xor m1 = u0 xor u1 
    % we also know that m0 xor m1 = 0xf (since m is chosen that way)
    delta_m = 15;
    
    % initialize the list of possible keys as empty
    key_list = [];
    
    % for all key guesses of key k1
    for key_guess = 0:15
       
        % invert the 2nd addroundkey
        v0 = bitxor(key_guess, c0(i));
        v1 = bitxor(key_guess, c1(i));
        
        % invert the sbox
        u0 = inv_sbox(v0);
        u1 = inv_sbox(v1);
        
        % compute the differential
        delta_u = bitxor(u0, u1);
        
        % check if delta_u is equal to delta_m (which is equal to 0xf)
        % if that is the case then keep the key_guess in the key_list
        if delta_u == delta_m
            key_list = [key_list key_guess];
        end
        
    end
    
    % we interesect among different plaintext/ciphertext pairs the key 
    % guesses that are valid
    if ~isempty(key_list)
       k1_recovered = intersect(k1_recovered, key_list); 
    end
    
    
end

% the resulting key is stored in key recovered
% compare it to the true key k1=7
k1_recovered == 7;

% using the recovered k1 we can also recover k0
k0_recovered = bitxor(inv_sbox(bitxor(c0(1), k1_recovered)), m0(1));
