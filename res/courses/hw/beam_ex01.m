%
% Beam Cantilever 


% pole souradnic
xz=[0, 0; 
    3, 0;
    6, 0];
% pole kodovych cisel
global lm=[1, 2, 3, 4,5,6;
	   4, 5, 6, 7,8,9];
%pocet prvku
nelem=2;
EA =1.0;
EI =1.0;
%nulovani vektoru zatizeni, matice tuhosti
f=zeros(9,1);
k=zeros(9);
r=zeros(9,1);

%sestaveni matic tuhosti
ke1=beam2d_stiffness([xz(1,1:2) xz(2,1:2)], EA, EI);
ke2=beam2d_stiffness([xz(2,1:2) xz(3,1:2)], EA, EI);
ke1
ke2
%lokalizace
k=assembly(k,ke1,1);
k=assembly(k,ke2,2);
k
%vektor zatizeni
f(8)=1;
%reseni posunuti
kuu=k(4:9,4:9);
fu=f(4:9);
u=kuu\fu;
%dopocteni reakci
R=k(1:3,4:9)*u;
R
%rekonstrukce celeho vektoru posunuti
r=[0;0;0;u];
r
r1=r(lm(1,:))
r2=r(lm(2,:))
%dopocteni uzlovych sil
s1 = beam2d_postpro([xz(1,1:2) xz(2,1:2)], EA, EI, r1)
s2 = beam2d_postpro([xz(2,1:2) xz(3,1:2)], EA, EI, r2)


