% CipherFour implementation
function c = cipher_four(m)

% set a fixed key for this cipher
key(1,:) = [10 7 5 0];
key(2,:) = [11 11 12 6];
key(3,:) = [3 5 7 0];
key(4,:) = [8 6 1 15];
key(5,:) = [6 12 4 4];
key(6,:) = [3 2 12 9];

% define the sbox
sbox = [6 4 12 5 0 7 2 14 1 15 3 13 8 10 9 11];

% define the bit permutation operation
perm = [1 5 9 13 2 6 10 14 3 7 11 15 4 8 12 16];

% initialize cipher's values
v = zeros(1,4);

% set the cipher state equal to the input plaintext
s = m;

% perform the cipher operations for 4 rounds
for round=1:4
    
    % addroundkey 
    u = bitxor(s, key(round,:));
    
    % sbox lookup
    for i=1:4
        v(i) = sbox(u(i)+1);
    end

    % permutation: careful with the row-wise bit-array reshaping and the
    % most-significant and least-significant bits
    t1 = de2bi(v,4,'left-msb');
    t2 = flip([t1(1,:) t1(2,:) t1(3,:) t1(4,:)]);
    t3 = flip(t2(perm));
    t4 = [t3(1:4); t3(5:8); t3(9:12); t3(13:16)]; 
    s = bi2de(t4,'left-msb')';

end

% perform the penultimate round key addition
u = bitxor(s, key(5,:));

% perform the last round sbox
for i=1:4
    s(i) = sbox(u(i)+1);
end

% perform the last round key addition
c = bitxor(s, key(6,:));


end