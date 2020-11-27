% funkce pocita matici prave strany od vlivu tepla (heat source) 2d prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   Q- teplo
%
% Out:
%   fe - matice prave strany (3,1)
%
function fe = heat2_source (xe,ye,Q) 

Ae = area_triangle(xe,ye) ;

fe = (Q*Ae/3)*[1; 1; 1]; 
end


