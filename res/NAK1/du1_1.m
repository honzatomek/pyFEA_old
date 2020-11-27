a=1.2;
b=0.8;
c=0.7;

nnode=12;
nelem=15;
neq=28;

xz=[	0., 0., 0., 2. + b;															% 1 - left column
		0., 2. + b, 0., 2. * (2. + b);											% 2
		0., 2. * (2. + b), 0., 3. * (2. + b);									% 3
		5. + a, 0., 5. + a, 2. + b;												% 4 - middle column
		5. + a, 2. + b, 5. + a, 2. * (2. + b);									% 5
		5. + a, 2. * (2. + b), 5. + a, 3. * (2. + b);						% 6
		8. + (2. * a), 0., 8. + (2. * a), 2. + b;								% 7 - right column
		8. + (2. * a), 2. + b, 8. + (2. * a), 2. * (2. + b);				% 8
		8. + (2. * a), 2. * (2. + b), 8. + (2. * a), 3. * (2. + b);		% 9
		0., 2. + b, 5. + a, 2. + b;												% 10 - bottom floor
		5. + a, 2. + b, 8. + (2. * a), 2. + b;									% 11
		0., 2. * (2. + b), 5. + a, 2. * (2. + b);								% 12 - middle floor
		5. + a, 2. * (2. + b), 8. + (2. * a), 2. * (2. + b);				% 13
		0., 3. * (2. + b), 5. + a, 3. * (2. + b);								% 14 - top floor
		5. + a, 3. * (2. + b), 8. + (2. * a), 3. * (2. + b)];				% 15

global lm=[	0, 0, 0, 2, 3, 4;
				2, 3, 4, 11, 12, 13;
				11, 12, 13, 20, 21, 22;
				0, 0, 1, 5, 6, 7;
				5, 6, 7, 14, 15, 16;
				14, 15, 16, 23, 24, 25;
				0, 0, 0, 8, 9, 10;
				8, 9, 10, 17, 18, 19;
				17, 18, 19, 26, 27, 28;
				2, 3, 4, 5, 6, 7;
				5, 6, 7, 8, 9, 10;
				11, 12, 13, 14, 15, 16;
				14, 15, 16, 17, 18, 19;
				20, 21, 22, 23, 24, 25;
				23, 24, 25, 26, 27, 28];

pload =[	0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., -20000. * c, 0.;
			0., -20000. * c, 0.;
			0., -10000. * c, 0.;
			0., -10000. * c, 0.;
			0., -15000. * c, 0.;
			0., -15000. * c, 0.];


promload =[	0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., 0., 0.;
				0., -1000., 0.;
				0., 0., 0.;
				0., -1000., 0.;
				0., -1000., 0.;
				0., 0., 0.;
				0., 0., 0.];

b1 = 0.3;
h1 = 0.3 + 0.1 * b;

b2 = 0.3;
h2 = 0.4 + 0.1 * a;

E = 2.5e10;		

A1 = b1 * h1;
A2 = b2 * h2;

I1 = 1/12 * b1 * h1 * h1 * h1;
I2 = 1/12 * b2 * h2 * h2 * h2;				

EA1 = E * A1;
EI1 = E * I1;
EA2 = E * A2;
EI2 = E * I2;

flok = zeros(6,1);
f=zeros(neq,1);
fp=zeros(neq,1);
k=zeros(neq);
ks=zeros(neq);
r=zeros(neq,1);


for i=1:9;
 kel=beam2d_stiffness(xz(i,:), EA1, EI1);
 k=assembly(k,kel,i);  
endfor;

for i=10:nelem;
 kel=beam2d_stiffness(xz(i,:), EA2, EI2);
 k=assembly(k,kel,i);  
endfor;


for i=1:nelem;
	flok = beam2d_load(xz(i,:), 0, pload(i,2));
	fp = assemblyf (fp, flok, lm, i);
endfor;

for i=1:nelem;
	%flok = zeros(6,1);
	flok = beam2d_load(xz(i,:), 0, promload(i,2));
	f = assemblyf (f, flok, lm, i);
endfor;

u=k\f
up=k\fp

s=zeros(nelem,1);
sp=zeros(nelem,1);

for i=1:nelem;
	r=zeros(6,1);
	rp=zeros(6,1);
	for j=1:6;
		 if lm(i,j) == 0
			 r(j)=0.0; 
			 rp(j)=0.0;   
		 else
			r(j)=u(lm(i,j));
			rp(j)=up(lm(i,j));
		endif;
	endfor;
	if i <= 9;
		EA = EA1;
		EI = EI1;
	else
		EA = EA2;
		EI = EI2;
	endif;
	endForces = beam2d_postpro(xz(i,:), EA, EI, r);
	s(i)=-endForces(1);
	endForces = beam2d_postpro(xz(i,:), EA, EI, rp);
	sp(i)=-endForces(1);
	
	i
	for j=1:6;
		if lm(i,j) == 0
			endForces(j)
		else
			lm(i,j)
			fp(lm(i, j)) - endForces(j)
		endif;
	endfor;

endfor;


#{
for i=10:nelem;
	r=zeros(6,1);
	rp=zeros(6,1);
	
	i
	
	for j=1:6;
		 if lm(i,j) == 0
			 r(j)=0.0; 
			 rp(j)=0.0;   
		 else
			r(j)=u(lm(i,j));
			rp(j)=up(lm(i,j));
		endif;
	endfor;
		
	endForces = beam2d_postpro ( xz(i, :), EA2, EI2, r);
	s(i)=-endForces(1);
	endForces = beam2d_postpro ( xz(i, :), EA2, EI2, rp);
	sp(i)=-endForces(1);
	endForces
endfor;
#}

for i=1:nelem;

 ksl=beam2d_initialstress(xz(i,:), sp(i));

 k=assembly(k,ksl,i);  

 ksl=beam2d_initialstress(xz(i,:), s(i));
 ks=assembly(ks,ksl,i);   
endfor;
[aa, bb, q, z, v, w, e]=qz(k,-ks);

[e,v]=sorteigval (abs(e),v);

r=v(:,1);
lr=(r'*k*r)/(r'*ks*r)

e

#{
for ei=1:4 
	clearplot
	hold on;
	axis ij;
	for i=1:nelem;
		beam2d_geoplot(xz(i,:)); 
	endfor;

	r=v(:,ei);
	for i=1:nelem;
		beam2d_defplot (xz(i,:), r, i); 
	endfor;

	hold off;
	pause;
endfor;
#}