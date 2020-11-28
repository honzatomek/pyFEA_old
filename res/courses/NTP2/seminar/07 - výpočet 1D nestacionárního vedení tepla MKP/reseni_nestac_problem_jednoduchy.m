% reseni nestacionarni ulohy vedeni tepla - jednoduchy proklad
% MKP

    clc

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     Z A D A N I  U L O H Y   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % pocatecni cas
    cas_poc = 0.0;
    
    % konecny cas
    cas_konec = 500000.0;
    
    % casovy krok
    delta_t = 1000.0;
    
    % tau
    tau = 0.5;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     K O N E C  Z A D A N I  U L O H Y   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     V Y P O C E T   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    
    cas = cas_poc;
    i = 1;
    while cas ~= cas_konec
        
        % matice leve strany
        a = (k*tau + c/delta_t);
    
        % vektor prave strany
        rhs = f*(1.0 - tau) + f*tau + (c/delta_t - k*(1.0 - tau))*r_old;
          
        % reseni soustavy rovnic pro stacionarni problem
        r = a\rhs;
        r_new = r;         
        
        r_old = r_new;
        
        % tisk do grafu:
        time(i) = cas;
        teplota_2(i) = r_new(1);
        teplota_3(i) = r_new(2);
        
        cas = cas + delta_t;
        i = i+1;
    end
    
    % tisk vyslednych neznamych
    r_new
    % tisk do grafu:
    plot(time,teplota_2,time,teplota_3);
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%     K O N E C   V Y P O C T U   %%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
   
 
   
   