% reseni 1. az 3. prikladu ze 3. cviceni
% overeni lokalizace a vypoctu prave strany pro vypocet stacionarniho vedeni
% MKP
  
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
    cn = [0 1 2 3];
    
    % pole Dirichletovych okr. podminek
    d = [5.0 0 0 0.0];
    
    % pole Neumannovych okr. podminkek
    fn = [0 0 0 5];
    
    % pole Cauchyho okr. podminkek
    fc = [0 0 0 0];
    
    %pole soucinitelu prestupu
    alfa = [4.0 4.0 4.0 4.0];
    
    % pocet neznamych
    n = 3;
    
    k = zeros(n,n);
    c = zeros(n,n);
    xe = zeros(2,1);
    ke = zeros(2,2);
    ce = zeros(2,2);
    de = zeros(2,1);
    ne = zeros(2,1);
    che = zeros(2,1);
    f = zeros(n,1);
   
    for i=1:3
        ia = up(i,1);
        ib = up(i,2);
        
        xe(1) = x(ia);
        xe(2) = x(ib);
        
        ke = matice_vodivosti (xe,lam(i));
        ce = matice_kapacity (xe,ro(i),ck(i));
        
        cne(1) = cn(ia);
        cne(2) = cn(ib);
        de(1) = d(ia);
        de(2) = d(ib);
        ne(1) = fn(ia);
        ne(2) = fn(ib);
        che(1) = fc(ia)*alfa(ia);
        che(2) = fc(ib)*alfa(ib);

        %matice konstruke
        k = lokalizace(k, ke, cne);
        c = lokalizace(c, ce, cne);
        
        %prava strana
        f = prava_strana_dirichlet (f, ke, de, cne);
        f = prava_strana_neumann (f, ne, cne);
        f = prava_strana_cauchy (f, che, cne);
        
        %prispevek od Cauchyho okr. podminky do matice vodivosti
        %k = ??
    end                 
   k
   c
   f
   
 %reseni soustavy rovnic pro stacionarni problem
 r = k\f;
 r
 
  
   
   
 
   
   