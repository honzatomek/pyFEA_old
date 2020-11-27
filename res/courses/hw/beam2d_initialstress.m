% funkce pocita matici pocatecnich napeti ohybaneho prutu v globalnim s.s. (kirchhoff, 2d)
% In: 
%   x - vektor souradnic uzlu prvku (x1,z1,x2,z2)
%   N - normalova sila (tahova > 0)
% Out:
%   ks - matice tuhosti prvku (6,6)
%
% (c) B. Patzak, 2008
%

function ks = beam2d_initialstress (x,N) 

  l=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
  l2 = l*l;

  kl =(N/l)*[0.    0.        0.      0.     0.       0.;
             0.   6./5.    -l/10.    0.   -6./5.   -l/10.;
             0.  -l/10.   2.*l2/15.  0.    l/10.   -l2/30.;
             0.    0.        0.      0.     0.       0.;
             0.  -6./5.    l/10.     0.    6./5.    l/10.;
             0.  -l/10.   -l2/30.    0.    l/10.    2*l2/15.];

  kl(1,1) = min(abs(kl(2,2)), abs(kl(3,3)))/1000.0;
  kl(1,4) = -kl(1,1);
  kl(4,1) = kl (1,4);
  kl(4,4) = kl(1,1);

  t=beam2d_t (x);
  ks = (t')*kl*t;
endfunction


