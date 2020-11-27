% Priklad 2
% Konzola se spojitym zatizenim
% 1 kvadraticky prvek

x = sym('x','real');
N=2/16*[(x-2)*(x-4) , -2*x*(x-4) , x*(x-2) ]

figure (1);
hold on
ezplot(N(1),[0 4])
ezplot(N(2),[0 4])
ezplot(N(3),[0 4])
title('Bazove funkce')
hold off

B=diff(N)
BDB=20*B'*B
K=int(BDB,0,4)
f=2*int(N,0,4)
r=zeros(3,1) ;
r(1:2)=K(1:2,1:2)\f(1:2)'

eps=B*r
S=20*eps

figure (2);
hold on
subplot(2,1,1)
ezplot(N*r,[0 4])
title('Posuny')
%
subplot(2,1,2)
ezplot(S,[0 4])
title('Normalova sila')
hold off

subs(S,x,4)