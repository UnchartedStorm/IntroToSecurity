% inverse sbox function
function y = inv_sbox(x)

inv_sbox = [4,8,6,10,1,3,0,5,12,14,13,15,2,11,7,9];

y = inv_sbox(x+1);

end
