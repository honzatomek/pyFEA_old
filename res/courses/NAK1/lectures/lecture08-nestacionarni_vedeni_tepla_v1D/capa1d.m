% funkce pocita matici kapacity prutu v 1d 
% In: 
%   x - vektor souradnic uzlu prvku (x1,x2)
%   c - koeficient tepelne kapacity
%
% Out:
%   ke - matice kapacity prvku (2,2)
%
function ke = capa1d (x,c) 

length=x(2)-x(1);
ke=(c*length)*[1./3. 1./6.; 1./6. 1./3.];
end


