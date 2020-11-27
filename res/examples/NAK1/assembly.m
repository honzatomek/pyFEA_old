% funkce pro lokalizaci matice tuhosti prvku 
% do matice tuhosti konstrukce
% vyzaduje existenci globalni matice kodovych cisel - lm
% 
%
% Vstup:
%   k - matice tuhosti konstrukce
%   ke- matice tuhosto prvku
%   e - cislo prvku 
%
% Vystup:
%   k - matice tuhosti konstrukce
%
% (c) B. Patzak, 2008
function k = assembly (k,ke,e)
	global lm;

	ndof = size(ke,1);
	for i=1:ndof
		  ia = lm(e,i);
		  if ia ~=0 
				for j=1:ndof
					 ja=lm(e,j);
					 if ja ~=0
						k(ia,ja)=k(ia,ja)+ke(i,j);
					 endif   
				endfor
		  endif
	endfor
endfunction