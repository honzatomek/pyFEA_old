% funkce sestavuje prispevek do matice vodivosti jednoho 1D prvku od
% cauchyho okr. podminek
 
  % vstup: 
  %      alfa  - vektor souc. prestupu tepla pro prvek
  
  % vystup:
  %      ke - matice vodivosti prvku (2,2)
  
  function ke = matice_vodivosti_cauchy (alfa)
    
    ke = alfa(1)*[1.0 0.0; 0.0 0.0] + alfa(2)*[0.0 0.0; 0.0 1.0];
        
  end      