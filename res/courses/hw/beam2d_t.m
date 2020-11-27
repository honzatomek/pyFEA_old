% funkce pocita transformacni matici (glob-> loc) 
% ohybaneho prutu v lokalnim s.s. 
% 
% (Rl = T*Rg)
% In: 
%   x - vektor souradnic uzlu prvku (x1,z1,x2,z2)
%
% Out:
%   t - transformacni matice (6,6)
%
% (c) B. Patzak, 2008
%
function t = beam2d_t (x) 
   
length=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
c = (x(3)-x(1))/length; 
s = (x(4)-x(2))/length; 

t=[ c s 0  0 0 0;
   -s c 0  0 0 0;
    0 0 1  0 0 0;
    0 0 0  c s 0;
    0 0 0 -s c 0;
    0 0 0  0 0 1];
endfunction


