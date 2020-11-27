x = sym('x','real');
N=[1-x/4, x/4 ]

figure (1);
hold on
ezplot(N(1),[0 4])
ezplot(N(2),[0 4])
title('Bazove funkce')
hold off

% Priklad 1
% Konzola zatizena silou
% 1 linearni prvek

B=diff(N)
BDB=20*B'*B
K=int(BDB,0,4)
f=[10 0] ;
r=zeros(2,1) ;
r(1)=K(1,1)\f(1)'

eps=B*r
S=20*eps

figure (2);
hold on
subplot(2,1,1)
ezplot(N*r,[0 4])
title('Posuny')
subplot(2,1,2)
axis([0 4 -12 0])
ezplot(S,[0 4])
title('Normalova sila')
hold off

subs(S,x,4)

% Priklad 2
% Konzola se spojitym zatizenim
% 1 linearni prvek

f=2*int(N,0,4)
r=zeros(2,1)
r(1)=K(1,1)\f(1)'

% presne reseni
u=1/20*(16-x*x) ;
F=-2*x

eps=B*r
S=20*eps

figure (3);
subplot(2,1,1)
hold on
axis([0 4 0 1])
X=[0:0.01:4];
NN=subs(N*r,x,X) ;
plot(X,NN,'b-','LineWidth',2)
uu=subs(u,x,X) ;
plot(X,uu,'r--','LineWidth',2)
title('Posuny')
hold off
%
subplot(2,1,2)
hold on
axis([0 4 -8 0])
X=[0:1:4];
f=subs(F,x,X) ;
plot(X,f,'r--','LineWidth',2)
s=subs(S,x,X) ;
plot(X,s,'b-')

title('Normalova sila')
hold off

subs(S,x,4)
