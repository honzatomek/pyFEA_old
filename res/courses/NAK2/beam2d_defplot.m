% plots beam2d deformed geometry
%
% In: 
%   xz pole souradnic uzlu (xz(nnodes, 2))
%   n1 cislo prvniho uzlu
%   n2 cislo druheho uzlu
%   i  cislo prvku
%   r  globalni vektor posunuti 
%
% Globals
%   lm pole kodovych cisel prvku
%
%
function beam2d_defplot (xz, r, i, n1, n2)

global lm;

% octave
plot ([xz(n1,1)+r(lm(i,1)) xz(n2,1)+r(lm(i,4))],[xz(n1,2)+r(lm(i,2)) xz(n2,2)+r(lm(i,5))], "-r");

%matlab
%plot ([xz(n1,1)+r(lm(i,1)) xz(n2,1)+r(lm(i,4))],[xz(n1,2)+r(lm(i,2)) xz(n2,2)+r(lm(i,5))]);

end
