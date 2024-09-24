% CipherTwo implementation
function c = cipher_two(m)

% set a fixed key for this cipher
k0 = 1;
k1 = 2;
k2 = 3;


% define the sbox
sbox = [6 4 12 5 0 7 2 14 1 15 3 13 8 10 9 11];

% addroundkey 
u = bitxor(m, k0);

% sbox lookup
v = sbox(u+1);

% addroundkey
w = bitxor(v, k1);

% sbox lookup
x = sbox(w+1);

% addroundkey
c = bitxor(x, k2);

end