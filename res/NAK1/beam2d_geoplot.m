% plots beam 2d geometry
%
% In: 
%   xz pole souradnic prvku (x1 z1 x2 z2)
%
% (c) B. Patzak, 2008
%

function beam2d_geoplot (xz)

plot ([xz(1) xz(3)],[xz(2) xz(4)], "-b");
endfunction;
