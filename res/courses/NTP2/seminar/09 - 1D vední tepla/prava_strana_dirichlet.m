% funkce sestavuje prispevek od Dirichletovy okr. podminky jednoho 1D prvku do prave strany pro celou konstrukci

    % vstup: 
        %    f - vektor prave strany
    %       ke - matice vodivosti jednoho prvku
    %       de - vektor dirichletovy okrajove podminky jednoho prvku
    %      cne - vektor kodovych cisel jednoho prvku

    function f = prava_strana_dirichlet (f, ke, de, cne)
            
                for i=1:2
                     r=cne(i);
                     if r ~= 0
                        for j=1:2
                           f(r) = f(r) - ke(i,j)*de(j);
                        end
                     end
                end
    end   
