% DFA assignment
clear all;
close all;

% load the faulty ciphtexts, the fault-free ciphertexts and the true
% key of round 16 from the file 'assignment_dfa.mat'


% repeat the process for n ciphertext pairs (C,C')
% for j=1:n

    % apply the inverse final permutation on C and C'
    

    % split the C and C' to left and right parts [L16, R16] and [L16', R16']
    

    % compute the fault differential Delta_R16 = R16 XOR R16'
   

    % compute the expansion E(L16)
    

    % compute the expansion E(L16')


    % apply the inverse permutation P to the fault differential
    

    % for all 8 DES sboxes
    % for i=1:8

        % in 'candidates' we will collect the correct key candidates
        % according to DFA equation
        % candidates = []; % initially the candidate list is empty

        % for all 2^6 key candidates of K_{16}^i
        % for k = 0:2^6-1      

            % select the parts corresponding to sbox Si

            % P^{-1}_{i}(Delta_R16) 
            

            % E_{i}(L16)


            % E_{i}(L16')


            % Compute the left and right part of the DFA equation and check
            % if the equation holds
          

            % if the key candidate agrees with the DFA equation then keep, 
            % otherwise discard it
            
        

        % For the first pair (C,C'), keep all valid key candidates.  
        % For the following pairs update the list of possible K_{16}^i
        % candidates by using intersection
        



        
        
        
        
        
        
% Finally, check if the recovered 16th roundkey of DES matches the true
% 16th round key loaded from 'assignment_dfa.mat'




    



