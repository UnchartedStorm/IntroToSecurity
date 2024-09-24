% Differential Cryptanalysis on CipherThree
clear all;
close all;

% generate plaintexts with difference equal to 0xf

% initialize to zero the key guess counter

% for all plaintext pairs
    
    % compute the respective ciphertext pairs using cipher_three()   
    
    % delta_m = m0 xor m1 = 0xf
    
    % we know that delta_u is equal to delta_m 
    
    % from the difference distribution of the sbox we also know that when 
    % delta_u=0xf, then delta_v is likely to be 0xd with probability 10/16
    
    % we know that delta_w is equal to delta_v 
    
    % from the difference distribution of the sbox we also know that when 
    % delta_w=0xd, then delta_x is likely to be 0xc with probability 6/16   
    
    % we know that delta_y is equal to delta_x 
    
    % assuming independent rounds compute the probability for the 
    % differential characteristic 0xf -> 0xd -> 0xc
    
    
    % for all key guesses of key k3
    
       
        % invert the 4th addkey operation        
        
        % invert the sbox        
        
        % compute the differential delta_y under the key hypothesis    
        
        % check if delta_y's match 
        
    
    
        


% recover the key k3 by finding which key guess has the largest counter

% compare it to the true k3 key specified in cipher_three()

% visualize with a bar plot the counters for the k3 key guesses

