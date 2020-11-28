% funkce sestavuje prispevek od Cauchyho okr. podminky jednoho 1D prvku do prave strany pro celou konstrukci

    % vstup: 
    %        f - vektor prave strany
    %       ce - vektor Cauchyho okrajove podminky jednoho prvku
    %      cne - vektor kodovych cisel jednoho prvku

    function f = prava_strana_cauchy (f, ce, cne)
            
                for i=1:2
                     r=cne(i);
                     if r ~= 0
                     f(r) = f(r) + ce(i);
                     end
                end
    end   
