% DFA assignment
clear all;
close all;

% load the faulty ciphtexts, the fault-free ciphertexts and the true
% key of round 16 from the file 'assignment_dfa.mat'
load("assignment_dfa.mat");

K16i = cell(1,8);

% repeat the process for n ciphertext pairs (C,C')
% for j=1:n
for j=1:10
    C = correct_ciphertext(j,:);
    F = faulty_ciphertext(j,:);

    % apply the inverse final permutation on C and C'
    C_inv = inverse_final_permutation(C);
    F_inv = inverse_final_permutation(F);

    % split the C and C' to left and right parts [L16, R16] and [L16', R16']
    C_L16 = C_inv(1:32);
    C_R16 = C_inv(33:64);
    F_L16 = F_inv(1:32);
    F_R16 = F_inv(33:64);

    % compute the fault differential Delta_R16 = R16 XOR R16'
    delta_R16 = bitxor(C_R16, F_R16);

    % compute the expansion E(L16)
    E_L16_C = expansion(C_L16);

    % compute the expansion E(L16')
    E_L16_F = expansion(F_L16);


    % apply the inverse permutation P to the fault differential
    delta_R16_inv = inverse_feistel_permutation(delta_R16);


    % for all 8 DES sboxes
    % for i=1:8
    for i=1:8

        % in 'candidates' we will collect the correct key candidates
        % according to DFA equation
        candidates = []; % initially the candidate list is empty

        % for all 2^6 key candidates of K_{16}^i
        for k = 0:2^6-1

            % select the parts corresponding to sbox Si

            % P^{-1}_{i}(Delta_R16)
            P_i_prev = delta_R16_inv((i-1)*4+1:i*4);

            % E_{i}(L16)
            E_i_L16_C = E_L16_C((i-1)*6+1:i*6);

            % E_{i}(L16')
            E_i_L16_F = E_L16_F((i-1)*6+1:i*6);

            % compute the 6-bit key candidate
            K_i = de2bi(k, 6);

            % Compute the left and right part of the DFA equation and check
            % if the equation holds
            rhs = bitxor(sboxf(bitxor(E_i_L16_C, K_i), i), sboxf(bitxor(E_i_L16_F, K_i), i));

            % if the key candidate agrees with the DFA equation then keep,
            % otherwise discard it
            if isequal(rhs, P_i_prev)
                candidates(end+1, :) = k;
            end



        end
        % For the first pair (C,C'), keep all valid key candidates.
        % For the following pairs update the list of possible K_{16}^i
        % candidates by using intersection
        if j == 1
            K16i{i} = candidates;
        else
            K16i{i} = intersect(K16i{i}, candidates);
        end
    end
end




% Finally, check if the recovered 16th roundkey of DES matches the true
% 16th round key loaded from 'assignment_dfa.mat'
recovered_key = cell2mat(K16i);
all(recovered_key == roundkey16_true)






