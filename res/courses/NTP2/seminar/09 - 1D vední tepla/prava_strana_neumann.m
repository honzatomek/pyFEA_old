% funkce sestavuje prispevek od Neumannovy okr. podminky jednoho 1D prvku do prave strany pro celou konstrukci

    % vstup: 
    %        f - vektor prave strany
    %       ne - vektor Neumannovy okrajove podminky jednoho prvku
    %      cne - vektor kodovych cisel jednoho prvku

    function f = prava_strana_neumann (f, ne, cne)
            
             for i=1:2
                    r=cne(i);
                  if r ~= 0
                         f(r) = f(r) + ne(i);
                  end
             end
    end   
