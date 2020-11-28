% funkce sestavuje matici vodivosti jednoho 1D prvku
 
  % vstup: 
  % x      - vektor souradnic prvku (x1,x2)
  % lambda - souc. tepl. vodivosti
  
  % vystup:
  %ke - matice vodivosti prvku (2,2)
  
  function ke = matice_vodivosti (x, lambda)
    
           l = x(2) - x(1);
           ke = (lambda/l)*[1.0 -1.0; -1.0 1.0];
  end         