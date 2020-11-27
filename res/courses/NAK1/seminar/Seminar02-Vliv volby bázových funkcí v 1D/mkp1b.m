% Priklad 2
% Konzola se spojitym zatizenim
% 2 linearni prvky

x = sym('x','real');
N=[1-x/2, x/2 ]

figure (1);
axis([0 4 0 1])
hold on
X=[0 2 ;0 2 ;2 4 ;2 4];
Y=[1 0 ;0 1 ;1 0 ;0 1];
plot(X(1,:),Y(1,:));
plot(X(2,:),Y(2,:));
plot(X(3,:),Y(3,:));
plot(X(4,:),Y(4,:));
title('Bazove funkce')
hold off

B=diff(N)
BDB=20*B'*B
Ki=int(BDB,0,2)
K=zeros(3,3) ;
K(1:2,1:2)=Ki ;
K(2:3,2:3)=K(2:3,2:3)+Ki ;
K
fi=2*int(N,0,2)
f=zeros(1,3);
f(1:2)=fi;
f(2:3)=f(2:3)+fi;
f
r=zeros(3,1) ;
r(1:2)=K(1:2,1:2)\f(1:2)'

% presne reseni
u=1/20*(16-x*x) ;
F=-2*x

figure (2);
subplot(2,1,1)
hold on
X=[0 2 4 ];
plot(X,r,'b-','LineWidth',2) ;
X=[0:0.01:4];
uu=subs(u,x,X) ;
plot(X,uu,'r--','LineWidth',2)
title('Posuny')
hold off
%
S1=subs(20*B*r(1:2),x,0)
S2=subs(20*B*r(2:3),x,2)
%
subplot(2,1,2)
hold on
axis([0 4 -8 0])
X=[0 2 2 4 ];
Y=[S1 S1 S2 S2];
plot(X,Y,'b-','LineWidth',2);
X=[0:1:4];
f=subs(F,x,X) ;
plot(X,f,'r--','LineWidth',2)

title('Normalova sila')
hold off
