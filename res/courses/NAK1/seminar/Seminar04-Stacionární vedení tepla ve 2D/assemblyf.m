% funkce pro lokalizaci matice prave strany 
% vyzaduje existenci globalni matice kodovych cisel - lm
% 
%
% Vstup:
%   f - matice prave strany
%   fe- matice prave strany prvku
%   lm- matice kodovych cisel
%   e - cislo prvku 
%
% Vystup:
%   f - matice prave strany
%
function f = assemblyf (f,fe,lm,e)

ndof = size(fe,1);
for i=1:ndof
        ia = lm(e,i);
        if ia ~=0 
           f(ia,1)=f(ia,1)+fe(i,1);
        end
    end
end