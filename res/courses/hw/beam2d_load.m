% funkce pocita vektor zatizeni od rovnomerneho spojiteho zatizeni
% In: 
%   x - vektor souradnic uzlu prvku (x1,z1,x2,z2)
%   fx- intenzita zatizeni podel prutu 
%   fz- intenzita zatizeni kolmo k prutu
% Out:
%   f - vektor zatizeni v globalni s.s.(6)
%
% (c) B. Patzak, 2014
%
function f = beam2d_load (x,fx,fz)
   
   l=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
   l2 = l/2.0;
   fl = [fx*l2; fz*l2; -1./12.*fz*l*l; fx*l2; fz*l2;  1./12.*fz*l*l];
    
   t=beam2d_t (x);
   f = t'*fl;
endfunction