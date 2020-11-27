% funkce pocita matici prave strany od predepsaneho konstatniho toku (heat flux) 2d prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   q- predepsany tok
%   b1,b2,b3 - hranice, kde je predepsany tok, voli se hodnoty 0 nebo 1
%
% Out:
%   ff - matice prave strany (3,1)
%
function ff = heat2_flux (xe,ye,q,b1,b2,b3) 

le = length_triangle(xe,ye);

ff = -q*(b1*[ le(1)/2 ; le(1)/2 ; 0] + b2*[ 0 ; le(2)/2 ; le(2)/2] + b3*[ le(3)/2 ; 0 ; le(3)/2 ]);
end


