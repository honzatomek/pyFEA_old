% plots beam2d deformed geometry
%
% In: 
%   xz pole souradnic uzlu prutu (x1 z1 x2 z2)
%   n1 cislo prvniho uzlu
%   n2 cislo druheho uzlu
%   i  cislo prvku
%   r  globalni vektor posunuti 
%
% Globals
%   lm pole kodovych cisel prvku
%
% (c) B. Patzak, 2008
function beam2d_defplot (xz, r, i)

	global lm;

	if lm(i,1) == 0
	  u1=0.0;
	else 
	  u1=r(lm(i,1));
	endif;
       
	if lm(i,4) == 0
	  u2 = 0.0;
	else 
	  u2 = r(lm(i,4));
	endif

	if lm(i,2) == 0
	  w1 = 0.0;
	else
	  w1 = r(lm(i,2));
	endif

	if lm(i,5) == 0
	  w2 = 0.0;
	else
	  w2=r(lm(i,5));
	endif

plot ([xz(1)+u1 xz(3)+u2],[xz(2)+w1 xz(4)+w2], "-r");
endfunction;
