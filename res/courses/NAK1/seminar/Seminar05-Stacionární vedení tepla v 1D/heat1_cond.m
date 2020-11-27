% funkce pocita matici vodivosti (conductivity matrix) 1d prvku s linearni aproximaci (heat1d)
% In: 
%   x - vektor souradnic uzlu prvku (x1,x2)
%   c- koeficient teplotni vodivosti
%
% Out:
%   ke - matice vodovosti prvku (2,2)
%
function ke = heat1_cond (x,c) 

length=(x(2)-x(1))

ke=(c/length)*[1.0 -1.0;
               -1.0 1.0];
end


