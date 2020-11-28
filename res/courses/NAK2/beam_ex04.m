%
% Beam structure 
%
% Globalni promenne
global nnode
global nelem;
global ndof;
global nelnode;
global neq; 
global uneq; 
global pneq;

global id; global lm;
global bc; global elnode;

%nastavime pocet uzlu, prvku, stupnu volnosti v uzlech, pocet uzlu prvku
nnode = 4; nelem=3; ndof=3; nelnode=2;

% pole souradnic uzlu
xz=[0, 3; 
    0, 0;
    4, 0;
    4, 3];
% pole kodovych cisel uzlu (0 volny posun, 1 podpora)
bc=[1,1,1;
    0,0,0;
    0,0,0;
    1,1,1];
% pole uzlu prvku
elnode=[1 2;
        2 3;
        3 4];
%charakteristiky prutu
EA =1.0;
EI =1.0;

%preprocessing - cislovani neznamych
preproc;

%kontrolni tisk
id
lm

%nulovani vektoru zatizeni, matice tuhosti
f=zeros(neq,1);
k=zeros(neq);
r=zeros(neq,1);

%sestaveni matic tuhosti
%cyklus pres prvky
for i=1:nelem;
 kel=beam2d_stiffness([xz(elnode(i,1),:) xz(elnode(i,2),:)], EA, EI);
 k=assembly(k,kel,i);  %lokalizace
end;

%vektor zatizeni
f(7)=1;

%reseni posunuti
kuu=k(pneq+1:neq,pneq+1:neq);
fu=f(pneq+1:neq);
u=kuu\fu;

%dopocteni reakci
R=k(1:pneq,pneq+1:neq)*u;
R
%rekonstrukce celeho vektoru posunuti
r(pneq+1:neq) = u;
r

%dopocteni uzlovych sil
for i=1:nelem;
  ri=r(lm(i,:));
  si(i,:) = beam2d_postpro([xz(elnode(i,1),:) xz(elnode(i,2),:)], EA, EI, ri);
end;
si

%POSTPROCESSING
%
%plot geometry
hold on;
axis ij;
for i=1:nelem;
beam2d_geoplot(xz, elnode(i,1), elnode(i,2)); 
end;

%plot deformation
for i=1:nelem;
beam2d_defplot (xz, r, i, elnode(i,1), elnode(i,2)); 
end;

%plot M
for i=1:nelem;
%beam2d_valplot (xz, [-si(i,2);si(i,5)], elnode(i,1), elnode(i,2));
beam2d_valplot (xz, [-si(i,3);si(i,6)], elnode(i,1), elnode(i,2));
end;

hold off;
pause;

