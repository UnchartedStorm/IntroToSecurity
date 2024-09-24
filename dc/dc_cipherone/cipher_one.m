% CipherOne implementation
function c = cipher_one(m)

% set a fixed key for this cipher
k0 = 5;
k1 = 7;

% define the sbox
sbox = [6 4 12 5 0 7 2 14 1 15 3 13 8 10 9 11];

% addroundkey 
u = bitxor(m, k0);

% sbox lookup
v = sbox(u+1);

% addroundkey
c = bitxor(v, k1);

end