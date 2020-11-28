% funkce sestavuje matici kapacity jednoho 1D prvku
   
   % vstup:
   % x  - vektor souradnic uzlu (x1,x2)
   % ro - objemova hmotnost
   % c  - merna tepelna kapacita
   
   % vystup:
   % ce - matice kapacity (2,2)
   
   function ce = matice_kapacity (x, ro, c)
            
            l = x(2) - x(1);
            ce = (ro*c*l)*[1/3 1/6; 1/6 1/3];
   end         