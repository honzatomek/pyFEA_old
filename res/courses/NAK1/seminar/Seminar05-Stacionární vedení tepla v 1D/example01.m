%
% Cviceni 1/ Priklad 2


% pole souradnic
x =[0,    2.0; 
    2.0 , 4.0];
% pole kodovych cisel
global lm=[1,2; 2,3];
%pocet prvku
nelem=2;
lambda =2.0;
a = 0.1;
%nulovani vektoru zatizeni, matice tuhosti
f=zeros(3,1);
k=zeros(3);
r=zeros(3,1);

%sestaveni matice vodivoosti
ke1=heat1_cond([x(1,1:2)], lambda);
ke2=heat1_cond([x(2,1:2)], lambda);
ke1
ke2
%lokalizace
k=assembly(k,ke1,1);
k=assembly(k,ke2,2);
k
%vektor prave strany
f(1)=5*1/a;
f(2)=5*2/a;
f(3)=5*1/a-5.0;
f
%reseni teploty
kuu=k(2:3,2:3);
fuu=f(2:3);
u=kuu\fuu;
u

