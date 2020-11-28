% reseni 1. az 3. prikladu ze 3. cviceni
% overeni lokalizace a vypoctu prave strany a 
% overeni casove diskretizace a reseni nestacionarniho vedeni tepla
% (linearni uloha)
% MKP

    clc

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     Z A D A N I  U L O H Y   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % pozn. zpusob zadani lze upravit dle pozadavku uzivatele a velikosti ulohy 
    
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
    cn = [1 2 3 4];
    
    
    % pole Dirichletovych okr. podminek POZOR! pouze tam, kde je podminka prdepsana
    d = [0.0 0 0 0.0];
    
    
    % pole Neumannovych okr. podminkek POZOR! pouze tam, kde je podminka prdepsana
    fn = [0 0 0 0];
    
    
    % pole Cauchyho okr. podminkek POZOR! pouze tam, kde je podminka prdepsana
    fc = [20.0 0 0 20.0];
    % pole soucinitelu prestupu POZOR! pouze tam, kde je podminka prdepsana
    alfa = [4.0 0.0 0.0 4.0];
    
    
    % pole pocatecnich podminek
    t_poc = [2.0 2.0 2.0 2.0];
    
    
    % pocatecni cas
    cas_poc = 0.0;
    
    % konecny cas
    cas_konec = 500000.0;
    
    % casovy krok
    delta_t = 1000.0;
    
    % tau
    tau = 0.5;
    
    % pocet uzlu
    nu = 4;
    
    % pocet prvku
    nelem = 3;
    
    % pocet neznamych
    n = 4;
    
    out = fopen('vysledek.dat','w');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     K O N E C  Z A D A N I  U L O H Y   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     V Y P O C E T   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    k = zeros(n,n);
    c = zeros(n,n);
    xe = zeros(2,1);
    ke = zeros(2,2);
    ce = zeros(2,2);
    de = zeros(2,1);
    ne = zeros(2,1);
    che = zeros(2,1);
    f = zeros(n,1);
    rhs = zeros(n,1);
    a = zeros(n,n);
    r_new = zeros(n,1);
    r_old = zeros(n,1);
    r = zeros(n,1);
    alfa_e = zeros(2,1);
   
    for i=1:nelem
        ia = up(i,1);
        ib = up(i,2);
        
        xe(1) = x(ia);
        xe(2) = x(ib);
        
        % matice vodivosti jednoho prvku
        ke = matice_vodivosti (xe,lam(i));
        
        %matice kapacity jednoho prvku
        ce = matice_kapacity (xe,ro(i),ck(i));
        
        cne(1) = cn(ia);
        cne(2) = cn(ib);
        de(1) = d(ia);
        de(2) = d(ib);
        ne(1) = fn(ia);
        ne(2) = fn(ib);
        che(1) = fc(ia)*alfa(ia);
        che(2) = fc(ib)*alfa(ib);

        % matice konstruke
        % matice vodivosti
        k = lokalizace(k, ke, cne);
        % matice kapacity
        c = lokalizace(c, ce, cne);
        
        % prava strana
        f = prava_strana_dirichlet (f, ke, de, cne);
        f = prava_strana_neumann (f, ne, cne);
        f = prava_strana_cauchy (f, che, cne);
        
        % prispevek od Cauchyho okr. podminky do matice vodivosti
        alfa_e(1) = alfa(ia);
        alfa_e(2) = alfa(ib);
        ke = matice_vodivosti_cauchy (alfa_e);
        % lokalizace
        k = lokalizace(k, ke, cne);
        
    end                 
    k
    c
    f
   
   
    % casova diskretizace pro linearni ulohu
    % pocatecni podminky
    j = 1;
    for i=1:nu
        if (cn(i) ~= 0)
            r_old(j) = t_poc(i); 
            j = j + 1;
        end
    end
    
    r_old
    
    cas = cas_poc;
    
    while cas ~= cas_konec
        
        % matice leve strany
        a = (k*tau + c/delta_t);
    
        % vektor prave strany
        rhs = f*(1.0 - tau) + f*tau + (c/delta_t - k*(1.0 - tau))*r_old;
          
        % reseni soustavy rovnic pro stacionarni problem
        r = a\rhs;
        r_new = r;         
        
        r_old = r_new;
        cas = cas + delta_t;
        
        % tisk v casovem kroku
        r_new
        fprintf(out,'%f  %f  %f  %f  %f\n',cas,r_new(1),r_new(2),r_new(3),r_new(4));
        
    end
        
    fclose(out);
    
    % tisk vyslednych neznamych
    r_new
  
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     K O N E C   V Y P O C T U   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
   
 
   
   