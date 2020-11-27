% funkce pocita matici vodivosti prutu v 1d 
% In: 
%   x - vektor souradnic uzlu prvku (x1,x2)
%   a - koeficient teplotni vodivosti
%
% Out:
%   ke - matice vodivosti prvku (2,2)
%
function ke = cond1d (x,a) 

length=x(2)-x(1);
ke=(a/length)*[1 -1; -1 1];
end


