% funkce pocita napeti na hrnach 2d trojuhelnikoveho stenoveho prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   sig - matice napeti v tezisti (3,1)
%
% Out:
%   pse - napeti na hranach (6,1)
%
function pse = boundary_stress (xe,ye,sig) 

pse = zeros(6,1) ;

A = [ sig(1), sig(3);
      sig(3), sig(2)] ;

y23 = ye(2)-ye(3); y31 = ye(3)-ye(1); y12 = ye(1)-ye(2);
x32 = xe(3)-xe(2); x13 = xe(1)-xe(3); x21 = xe(2)-xe(1);

le = length_triangle (xe,ye) ;

c1 = -y12/le(1) ;
s1 = -x21/le(1) ;

T = [ c1, s1; -s1, c1 ];

temp = T*A*[c1;s1];

pse(1) = temp(1,1) ;
pse(2) = temp(2,1) ;

c1 = -y23/le(2) ;
s1 = -x32/le(2) ;

T = [ c1, s1; -s1, c1 ];

temp = T*A*[c1;s1];

pse(3) = temp(1,1) ;
pse(4) = temp(2,1) ;

c1 = -y31/le(3) ;
s1 = -x13/le(3) ;

T = [ c1, s1; -s1, c1 ];

temp = T*A*[c1;s1];

pse(5) = temp(1,1) ;
pse(6) = temp(2,1) ;

end


