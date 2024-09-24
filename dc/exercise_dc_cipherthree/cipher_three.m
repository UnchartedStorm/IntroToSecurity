% CipherThree implementation
function c = cipher_three(m)

% set a fixed key for this cipher
k0 = 10;
k1 = 5;
k2 = 11;
k3 = 7;


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
y = bitxor(x, k2);

% sbox lookup
z = sbox(y+1);

% addroundkey
c = bitxor(z, k3);


end