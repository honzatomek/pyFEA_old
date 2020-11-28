% funkce pro vypocet vnitrnich sil na prvku beam2d
% In:
%   x - vektor souradnic uzlu prvku  (x1,z1,x2,z2)
%   EA- soucin modulu pruznosti a plochy
%   EI- coucin modulu pruznosti a momentu setrvacnosti
%   r - vektor uzlovych posunu prvku v glob s.s. (u1,w1,u2,w2)
%
% Out:
%   s   vektor koncovych sil a momentu
%
function s = beam2d_postpro (x,EA,EI,r) 


length=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
%local stiffness
kl = beam2d_stiffness_lcs (length, EA, EI);
%transformation matrix
t  = beam2d_t   (x);

s = kl*t*r;
end


