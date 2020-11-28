% funkce pocita matici tuhosti ohybaneho prutu v globalnim s.s. (kirchhoff, 2d)
% In: 
%   x - vektor souradnic uzlu prvku (x1,z1,x2,z2)
%   EA- soucin modulu pruznosti a plochy
%   EI- soucin modulu pruznosti a momentu setrvacnosti
%
% Out:
%   ke - matice tuhosti prvku (6,6)
%
function ke = beam2d_stiffness (x,EA, EI) 

length=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
%local stiffness
kl = beam2d_stiffness_lcs (length, EA, EI);
%transformation matrix
t  = beam2d_t   (x);

%transformation
ke=(t')*kl*t;

end


