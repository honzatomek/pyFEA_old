%
% Cviceni 5/ Priklad 2


%pocet prvku
nelem=4;
nnodes=5;
E=10; 
nu = 0.1;

% pole kodovych cisel uzlu
id = [ 5 6; 7 1; 8 2; 9 10; 3 4 ];

%pole uzlovych cisel prvku
ide = [1 2 5; 2 3 5; 3 4 5; 4 1 5];

% pocet neznamych
neq = 10;

% pole souradnic
x =[0.0, 6.0, 6.0, 0.0, 2.0];
y =[0.0, 0.0, 3.0, 3.0, 1.0];

ke = zeros(6,6);
dbe = zeros(3,6);
be = zeros(3,6);
de = zeros(3,3);

k = zeros(neq,neq);
f = zeros(neq,1);

for i = 1:nelem
    xe = [x(ide(i,:))] ;
    ye = [y(ide(i,:))] ;
    [ke,dbe,de,be] = plane_stress(xe,ye,E,nu) 
    lm = [id(ide(i,1),:), id(ide(i,2),:), id(ide(i,3),:)];
    k=assembly(k,ke,lm,1);
end

k
f = [ 1.5, 1.5, 0.0, 0.0] ;

%reseni posunu
kuu=k(1:4,1:4)
fuu=f(:)
u=kuu\fuu;
u

ug = zeros(neq,1);
ug(1:4)=u(:) 

%reseni relativnich deformaci a napeti

for i = 1:nelem
    xe = [x(ide(i,:))] ;
    ye = [y(ide(i,:))] ;
    [ke,dbe,de,be] = plane_stress(xe,ye,E,nu) ;
    lm = [id(ide(i,1),:), id(ide(i,2),:), id(ide(i,3),:)] ;
    ul = [ug(lm)] ;
    eps = be*ul
    sig = dbe*ul
    pse = boundary_stress (xe,ye,sig)
end

% Plot deformed configuration over the initial configuration
for i = 1:nnodes
    xnew(i) = x(i) + ug(id(i,1));
    ynew(i) = y(i) + ug(id(i,2));
end

figure; 
for i = 1:nelem
    xe = [x(ide(i,:))] ;
    ye = [y(ide(i,:))] ;
    plot(xe,ye,'k');hold on;
    xe = [xnew(ide(i,:))] ;
    ye = [ynew(ide(i,:))] ;
    plot(xe,ye,'r');hold on;
end
title('Initial and deformed structure'); xlabel('X'); ylabel('Y');

