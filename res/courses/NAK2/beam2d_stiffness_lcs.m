% funkce pocita matici tuhosti ohybaneho prutu v lokalnim s.s. (kirchhoff, 2d)
% In: 
%   l - delka
%   EA- soucin modulu pruznosti a plochy
%   EI- soucin modulu pruznosti a momentu setrvacnosti
%
% Out:
%   ke - matice tuhosti prvku (6,6)
%
function ke = beam2d_stiffness_lcs (l,EA, EI) 

   l2=l*l;
   l3=l2*l;
   ke=[EA/l      0.         0.     -EA/l        0.         0.;
	 0    12.*EI/l3 -6.*EI/l2    0.    -12.*EI/l3  -6.*EI/l2;
	 0   -6.*EI/l2   4.*EI/l     0.    6.*EI/l2     2.*EI/l;
       -EA/l     0.         0.      EA*l        0.         0.;
	 0.   -12.*EI/l3 6.*EI/l2   0.    12.*EI/l3    6.*EI/l2;
	 0.   -6.*EI/l2  2.*EI/l    0.    6.*EI/l2     4.*EI/l];

end


