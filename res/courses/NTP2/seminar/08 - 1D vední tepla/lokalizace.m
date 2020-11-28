% funkce lokalizuje matici 1D prvku do matice konstrukce

    % vstup:
    % m  - matice vodivosti/kapacity konstrukce
    % me - matice vodivosti/kapacity jednoho prvku
    % cne - vektor kodovych cisel jednoho prvku
    
    function m = lokalizace (m, me, cne)
      
             for i=1:2
                 r=cne(i);
                 if r ~= 0
                    for j=1:2
                        s=cne(j);
                        if s ~= 0
                           m(r,s)=m(r,s)+me(i,j);
                        end   
                    end
                 end
             end
    end