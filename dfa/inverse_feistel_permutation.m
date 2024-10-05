% DES inverse feistel permutation P^{-1}(c)
function result = inverse_feistel_permutation(x)
  inv_feistel =  [9  17  23  31  13  28  2  18 ...
                  24  16  30  6  26  20  10  1 ...
                  8  14  25  3  4  29  11  19 ...
                  32  12  22  7  5  27  15  21];

  result = x(inv_feistel);

end