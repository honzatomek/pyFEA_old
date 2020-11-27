% funkce pocita matici prave strany od pprenosu tepla (newton condition) 2d prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   alpha- koeficient prestupu
%   b1,b2,b3 - hranice, kde je predepsany tok, voli se hodnoty 0 nebo 1
%
% Out:
%   ff - matice prave strany (3,3)
%
function ff = heat2_newton (xe,ye,alpha,b1,b2,b3) 

le = length_triangle(xe,ye);

ff = zeros (3,3) ;
ff = ff+alpha*b1*le(1)*[1/3,1/6,0; 1/6,1/3,0; 0,0,0] ;
ff = ff+alpha*b2*le(2)*[ 0,0,0; 0,1/3,1/6; 0,1/6,1/3] ;
ff = ff+alpha*b3*le(3)*[ 1/3,0,1/6; 0,0,0; 1/6,0,1/3] ;
    
end


