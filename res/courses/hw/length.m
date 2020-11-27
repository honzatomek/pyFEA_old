% pocita delku prvku
% x = vektor koncovych souradnic {x1, z1, x2, z2}


function l=length(x)
   
   l=sqrt((x(3)-x(1))^2+(x(4)-x(2))^2);
	
endfunction;