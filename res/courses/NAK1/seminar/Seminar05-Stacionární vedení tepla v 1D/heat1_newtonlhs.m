% funkce pocita prispevek do leve strany rovnice of newtonovy okrajove podminky (prestup tepla) (heat1d)
% In: 
%   id - cislo lokalniho uzlu, kde je okrajova podm. aplikovana
%   lambda- koeficient prestupu tepla
%
% Out:
%   ke - matice vodovosti prvku (2,2)
%
function ke = heat1_newtonlhs (id,alpha) 

ke=zeros(2);
ke(id,id) = alpha;
end



