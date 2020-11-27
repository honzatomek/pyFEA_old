% funkce pocita plochu trojuhelnikoveho prvku
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%
% Out:
%   Ae - plocha prvku
%
function Ae = area_triangle (xe,ye) 

Ae=(1/2)*((xe(2)*ye(3)-xe(3)*ye(2))-(xe(1)*ye(3)-xe(3)*ye(1))+(xe(1)*ye(2)-xe(2)*ye(1))) ;
end


