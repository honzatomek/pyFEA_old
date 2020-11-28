% overeni lokalizace matice vodivosti a kapacity pro 1D vedeni tepla
  
    clc

    % pole souradnic
    x = [0.0 0.1 0.2 0.3];
    
    % pole vodivosti
    lam = [2.0 2.0 2.0];
    
    % pole obj. hmotnosti
    ro = [2500.0 2500.0 2500.0];
    
    % pole merne tepelne kapacity
    ck = [1000.0 1000.0 1000.0];
    
    % pole uzlu prvku
    up = [1 2; 2 3; 3 4];
    
    % pole kodovych cisel
    cn = [0 1 2 0];
    
    k = zeros(2,2);
    c = zeros(2,2);
    xe = zeros(2);
    ke = zeros(2,2);
    ce = zeros(2,2);
   
    for i=1:3
        ia = up(i,1);
        ib = up(i,2);
        xe(1) = x(ia);
        xe(2) = x(ib);
        ke = matice_vodivosti (xe,lam(i));
        ce = matice_kapacity (xe,ro(i),ck(i));
        cne(1) = cn(ia);
        cne(2) = cn(ib);
        k = lokalizace(k, ke, cne);
        c = lokalizace(c, ce, cne);
    end                 
   k
   c
   
    
  
  
   
   
 
   
   