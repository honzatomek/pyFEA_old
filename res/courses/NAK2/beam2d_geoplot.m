% plots beam 2d geometry
%
% In: 
%   xz pole souradnic uzlu (xz(nnodes, 2))
%   n1 cislo prvniho uzlu
%   n2 cislo druheho uzlu
%
function beam2d_geoplot (xz, n1, n2)

% octave 
plot ([xz(n1,1) xz(n2,1)],[xz(n1,2) xz(n2,2)], "-b");

% matlab
% plot ([xz(n1,1) xz(n2,1)],[xz(n1,2) xz(n2,2)],'-sk');

end
