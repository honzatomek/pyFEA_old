% funkce pocita matici tuhosti 2d trojuhelnikoveho stenoveho prvku s linearni aproximaci
% In: 
%   xe - vektor x-ovych souradnic uzlu prvku (x1,x2,x3)
%   ye - vektor y-ovych souradnic uzlu prvku (y1,y2,y3)
%   E - Younguv modul pruznosti
%   nu - Poissonuv soucinitel
%
% Out:
%   ke - matice tuhosti prvku (6,6)
%   dbe - matice na vypocet napeti (3,6)
%   de - materialova matice (3,3)
%   be - mative derivaci bazovych funkci (3,6)
%
function [ke,dbe,de,be] = plane_stress (xe,ye,E,nu) 

Ae = area_triangle(xe,ye) ;

y23 = ye(2)-ye(3); y31 = ye(3)-ye(1); y12 = ye(1)-ye(2);
x32 = xe(3)-xe(2); x13 = xe(1)-xe(3); x21 = xe(2)-xe(1);

be = (1/(2*Ae))*[ y23, 0, y31, 0, y12, 0 ;
                  0, x32, 0, x13, 0, x21 ;
                  x32,y23,x13,y31,x21,y12] ;

de = (E/(1-nu*nu))*[ 1, nu, 0;
                    nu, 1, 0;
                    0, 0, (1-nu)/2 ];
                
dbe = de*be ;
              
ke = Ae*be'*dbe;

end


