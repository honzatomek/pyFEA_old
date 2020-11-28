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
function beam2d_valplot (xz, val, n1, n2)

%compute local z axis direction
dx=xz(n2,1)-xz(n1,1);
dz=xz(n2,2)-xz(n1,2);
n=[-dz;dx];
n=n/norm(n);

%octave
plot ([xz(n1,1) xz(n1,1)+n(1)*val(1) xz(n2,1)+n(1)*val(2) xz(n2,1)],
      [xz(n1,2) xz(n1,2)+n(2)*val(1) xz(n2,2)+n(2)*val(2) xz(n2,2)],
      "-r");

% matlab
%plot ([xz(n1,1) xz(n1,1)+n(1)*val(1) xz(n2,1)+n(1)*val(2) xz(n2,1)], %[xz(n1,2) xz(n1,2)+n(2)*val(1) xz(n2,2)+n(2)*val(2) xz(n2,2)], %'color', 'r') ;


end
