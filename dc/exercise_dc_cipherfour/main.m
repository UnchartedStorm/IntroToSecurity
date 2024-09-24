% Differential Cryptanalysis on CipherFour
clear all;
close all;


% Generate a few thousand 16-bit plaintexts pairs
% Each plaintext can be organized as 4 nibbles: [a b c d] 
% Note that a nibble is a 4-bit value
% Ensure that the difference between every plaintext pair (m0,m1) is 
% equal to (0 0 2 0)


% for all generated plaintext pairs 
    
    % compute the respective ciphertext pairs using the cipher_four()
    % implementation
   
    
    % apply filtering to the ciphertext pairs i.e. 
    % -compute the difference between the ciphertext pairs
    
    % -check if this difference could be originating from a correct pair
    % the correct pairs are: (0 0 h 0) where h is in {1,2,9,10} 
    
    % -if the ciphertext pair passes the filter's check, we keep it
    % otherwise, we discard it

    
% end

% focus on the 3rd nibble of the ciphertext pairs that were kept after
% filtering

% initalize the counter for all key candidates to zero


% for all ciphertexts that remain after filtering


    % for all key guesses of the 3rd nible of roundkey k6 
    
    
        % invert the 6th addkey operation
        

        % invert the sbox
        

        % compute the difference delta
       

        % compare the delta with the difference (0 0 2 0)
        % if they are equal then increment the the respective key counter
        % by one
 


% find which key guess has the largest counter 

% print and store the recovered key nibble
% you can also confirm by comparing it to the correct key nibble in
% cipher_four()

% visualize with a bar plot the counters for the k6 key guesses


