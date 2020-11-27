% funkce pocita matici vodivosti (conductivity matrix) 2d prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   c- koeficient teplotni vodivosti
%
% Out:
%   ke - matice vodovosti prvku (3,3)
%
function ke = heat2_cond (xe,ye,c) 

Ae = area_triangle(xe,ye) ;

Be = (1/(2*Ae))*[(ye(2)-ye(3)), (ye(3)-ye(1)), (ye(1)-ye(2));
                 (xe(3)-xe(2)), (xe(1)-xe(3)), (xe(2)-xe(1))]

ke = c*Ae*Be'*Be;

end


