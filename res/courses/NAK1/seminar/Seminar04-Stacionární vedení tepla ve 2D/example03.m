%
% Cviceni 4/ Priklad 3


%pocet prvku
nelem=2;
lambda =5.0;
alpha = 4.0;
Q = 6.0;
q2 = 20;

% pole kodovych cisel
lm = [1 2 3; 2 4 3];
% pocet neznamych
nu = 4;

% pole souradnic
x =[0.0, 2.0, 0.0, 2.0];
y =[0.0, 0.5, 1.0, 1.0];

ke = zeros(3,3);
k = zeros(nu,nu);
f = zeros(nu,1);

for i = 1:nelem
    xe = [x(lm(i,:))] ;
    ye = [y(lm(i,:))] ;
    ke = heat2_cond(xe,ye,lambda)
    k=assembly(k,ke,lm,i);
    fe = heat2_source(xe,ye,Q)
    f=assemblyf(f,fe,lm,i);
end

k
f

ff2 = heat2_flux (x(lm(2,:)),y(lm(2,:)),q2,0,1,0)
f=assemblyf(f,ff2,lm,2)

fn1 = heat2_newton (x(lm(1,:)),y(lm(1,:)),alpha,1,0,1)
k=assembly(k,fn1,lm,1);

%reseni teploty
kuu=k(1:4,1:4)
fuu=f(1:4)
u=kuu\fuu;
u

t = zeros(4,1);
t=u ;

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
