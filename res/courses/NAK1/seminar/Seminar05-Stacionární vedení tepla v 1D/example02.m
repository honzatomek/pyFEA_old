%
% Cviceni 1/ Priklad 2


% pole souradnic
x =[0,    4.0]; 
% pole kodovych cisel
global lm=[1,2];
%pocet prvku
nelem=1;
lambda =2.0;
alpha = 4
a = 0.1;
%nulovani vektoru zatizeni, matice tuhosti
f=zeros(2,1);
k=zeros(2);
r=zeros(2,1);

%sestaveni matice vodivosti
k=heat1_cond(x, lambda);
% prispevek od okrajovych podminek do lhs
lhsbc1=heat1_newtonlhs (2,alpha); 
lhsbc1
k=k+lhsbc1
%vektor prave strany
f(2)=alpha*20;
f
%reseni teploty
kuu=k(2:2,2:2);
fuu=f(2:2);
u=kuu\fuu;
u

