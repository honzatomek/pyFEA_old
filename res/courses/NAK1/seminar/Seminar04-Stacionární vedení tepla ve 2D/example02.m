%
% Cviceni 4/ Priklad 2


%pocet prvku
nelem=12;
lambda =5.0;
Q = 6.0;
q2 = 20;

% pole kodovych cisel
lm = [ 1 2 10;
       2 11 10;
       2 3 11;
       3 12 11;
       3 4 12;
       4 6 12;
       4 5 6;
       10 11 9;
       11 8 9;
       11 12 8;
       12 7 8;
       12 6 7];
% pocet neznamych
nu = 12;

% pole souradnic
x =[0, 0, 0, 0, 0, 1, 2, 2, 2, 1, 1, 1];
y =[1, 0.75, 0.5, 0.25, 0, 0.25, 0.5, 0.75, 1, 1, 0.75, 0.5];

ke = zeros(3,3);
k = zeros(nu,nu);
f = zeros(nu,1);

for i = 1:nelem
    xe = [x(lm(i,:))] ;
    ye = [y(lm(i,:))] ;
    ke = heat2_cond(xe,ye,lambda);
    k=assembly(k,ke,lm,i);
    fe = heat2_source(xe,ye,Q);
    f=assemblyf(f,fe,lm,i);
end

k
f

ff1 = heat2_flux (x(lm(1,:)),y(lm(1,:)),q2,0,0,1)
f=assemblyf(f,ff1,lm,1)
ff8 = heat2_flux (x(lm(8,:)),y(lm(8,:)),q2,0,0,1)
f=assemblyf(f,ff8,lm,8)

%reseni teploty
kuu=k(8:12,8:12)
fuu=f(8:12)
u=kuu\fuu;
u

t = zeros(12,1);
t(8:12)=u(:) ;

figure; 
for i = 1:nelem
  xe = [x(lm(i,:))] ;
  ye = [y(lm(i,:))] ;
  te = [t(lm(i,:))] ;
  XX 	= [xe(1) xe(2) xe(3) xe(1)];
  YY 	= [ye(1) ye(2) ye(3) ye(1)];
  tt 	= [te(1) te(2) te(3) te(1)];
  patch(XX,YY,tt);hold on;  
end
title('Temperature distribution'); xlabel('X'); ylabel('Y'); colorbar;
