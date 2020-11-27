% funkce pocita delky stran trojuhelnikoveho prvku
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%
% Out:
%   le - delky hran prvku (3,1)
%
function le = length_triangle (xe,ye) 

le = zeros(3,1) ;
le(1) = sqrt((xe(2)-xe(1))*(xe(2)-xe(1))+(ye(2)-ye(1))*(ye(2)-ye(1)));
le(2) = sqrt((xe(3)-xe(2))*(xe(3)-xe(2))+(ye(3)-ye(2))*(ye(3)-ye(2)));
le(3) = sqrt((xe(1)-xe(3))*(xe(1)-xe(3))+(ye(1)-ye(3))*(ye(1)-ye(3)));
end


