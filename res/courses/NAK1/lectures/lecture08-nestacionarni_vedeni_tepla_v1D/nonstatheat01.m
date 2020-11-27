%
% Nestacionarni vedeni tepla 
%pocet prvku
nnode=20; nelem=nnode-1;
neq=nnode;
a=1.0;
c=1.0;
tau=0.5;
dt=0.001;
nstep=400;
nplotstep=10;

global lm;
% pole souradnic
xyz=zeros(nnode,1);
for i=1:nnode; xyz(i)=(1./(nnode-1))*(i-1); end;
lm=zeros(nelem,2);
% pole kodovych cisel
for i=1:nelem; lm(i,1)=i; lm(i,2)=i+1; end;


%nulovani vektoru a matic 
kv=zeros(neq);
kc=zeros(neq);
r0=zeros(neq,1);
%delete graphics
cla
hold on;
plot (xyz, r0,'-ks','LineWidth',2);

%pocatecni podminky
for i=1:nnode
    r0(i)=cos(2*xyz(i));
    r1=r0;
end
plot (xyz, r0,'-rs');

%sestaveni matic vodivosti+capacity
kve=cond1d(xyz(1:2), a);
kke=capa1d(xyz(1:2), c);
for ie = 1:nelem
   kv=assembly (kv,kve,ie);
   kc=assembly (kc,kke,ie); 
end
A=tau*kv+(1/dt)*kc;
B=(tau-1)*kv+(1/dt)*kc;

for i=1:nstep
   r0=r1;
   r1=A\(B*r0);
   if (mod(i,nplotstep) == 0)
         plot (xyz, r1);
   end

end

hold off

