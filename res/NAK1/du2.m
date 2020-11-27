% plasticita
a=1.2;
b=0.8;
c=0.7;

nnode=8;
nelem=7;
neq=19;
statn=2;

xz=[	0., 0., 2. * a, 3. * b;						% 1 - sikmy sloup (a-b)
		6. * a, 0., 6. * a, 2. * b;				% 2 - pravy spodni sloup (d-h)
		6. * a, 2. * b, 6. * a, 3. * b;			% 3 - pravy prostredni sloup (h-c)
		6. * a, 3. * b, 6. * a, 4. * b;			% 4 - pravy horni sloup (c-f)
		0., 3. * b, 2. * a, 3. * b;				% 5 - levy pruvlak (e-b)
		2. *a, 3. * b, 3. * a, 3. * b;			% 6 - prostredni pruvlak (b-g)
		3. *a, 3. * b, 6. * a, 3. * b];			% 7 - pravy pruvlak (g-c)		

global lm=[	0,0,1,2,3,4;
				0,0,0,5,6,7;
				5,6,7,8,9,10;
				8,9,10,11,12,13;
				14,15,16,2,3,4;
				2,3,4,17,18,19;
				17,18,19,8,9,10];
				
secchar = [	1;
				1;
				1;
				1;
				2;
				2;
				2;];

load =[	0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., 0., 0.;
			0., -4000. * b, 0;
			0., -4000. * b, 0;
			0., -4000. * b, 0];

popis = ["a3",
			"b1",
			"b2",
			"b3",
			"h1",
			"h2",
			"h3",
			"c1",
			"c2",
			"c3",
			"f1",
			"f2",
			"f3",
			"e1",
			"e2",
			"e3",
			"g1",
			"g2",
			"g3"];
			
bs = 0.3;
hs = 0.3;

bp = 0.3;
hp = 0.4 * (0.9 + c/10.);

E = 3e10;		

EA = zeros(2,1);
EI = zeros(2,1);
Mpl = zeros(2,1);

EA = [E*bs*hs, E*bp*hp];
EI = [E*1/12*bs*hs*hs*hs, E*1/12*bp*hp*hp*hp];
Mpl = [100000. + (20000. * c), (1. + c) * (100000. + (20000. * c))];

f(4,1) = 20000. * c;
f(11,1) = 2000. * a;

tempxz = zeros(2,1);
templm = zeros(3,1);
e = zeros(nelem,1);
P = zeros(statn+1,1);
Mmax_1 = zeros(nelem, statn+1);
#{
for n=0:statn;

	if n>0;
		P(n) = p(1);
		if (Mmax(e(1),3) != 0);
			neq = neq+1;
			
			if Mmax(e(1),3) == 1;
				lm(e(1),3) = neq;
			else
				lm(e(1),6) = neq;
			endif;
			
			popis = resize(popis, neq, 2);
			
			popis(neq,1) = popis(e(1),1);
			popis(neq,2) = "4"
		
		else
			nnode = nnode + 1
			nelem = nelem + 1
			neq=neq+4
			
			tempxz(1)=xz(e(1),3);
			tempxz(2)=xz(e(1),4);
			
			xz = resize(xz, nelem, 4);
			
			l = length(xz(e(1),:));
			
			xz(e(1),3) = tempxz(1) + (tempxz(1) - xz(e(1),1)) * Mmax(e(1),2)/l;
			xz(e(1),4) = tempxz(2) + (tempxz(2) - xz(e(1),2)) * Mmax(e(1),2)/l;
			
			xz(nelem,1) = xz(e(1),3);
			xz(nelem,2) = xz(e(1),4);
			xz(nelem,3) = tempxz(1);
			xz(nelem,4) = tempxz(2)
			
			templm(1)=lm(e(1),4);
			templm(2)=lm(e(1),5);
			templm(3)=lm(e(1),6);
			
			lm = resize(lm, nelem, 6);
			
			lm(e(1),4) = neq - 3;
			lm(e(1),5) = neq - 2;
			lm(e(1),6) = neq - 1;
			
			lm(nelem,1) = lm(e(1),4);
			lm(nelem,2) = lm(e(1),5);
			lm(nelem,3) = neq;
			lm(nelem,4) = templm(1);
			lm(nelem,5) = templm(2);
			lm(nelem,6) = templm(3)
			
			load = resize(load, nelem, 3);
			load(nelem,:) = load(e(1),:)
			
			secchar = resize(secchar, nelem,1);
			secchar(nelem) = secchar(e(1));
			
			popis = resize(popis, neq, 2);
			
			for k=1:4;
				popis((neq-4)+k, :) = [n, k];
			endfor;
			
			popis

		endif;
	endif;
#}

	flok = zeros(6,1);
	f = zeros(neq,1);
	kel = zeros(6);
	k = zeros(neq);
	u = zeros(neq,1);

	for i=1:nelem;
		kel = beam2d_stiffness(xz(i,:), EA(secchar(i)), EI(secchar(i)));
		k = assembly(k, kel, i);
	endfor;

	for i=1:nelem;
		flok = beam2d_load(xz(i,:), load(i,1), load(i,2));
		f = assemblyf(f, flok, lm, i);
	endfor;

	f(4,1) = f(4,1) + 20000. * c;
	f(11,1) = f(11,1) + 2000. * a;

	u=k\f;

	for i=1:neq;
		popis(i,:)
		i;
		u(i)
	endfor;

	p = zeros(nelem,1);
	Mmax = zeros(nelem, 3);
	eForces = zeros(nelem, 6);
	endForces = zeros(6,1);
	t = zeros(6,6);
	eFor = zeros(6,1);

	for i=1:nelem;
		r=zeros(6,1);
		for j=1:6;
			 if lm(i,j) == 0
				 r(j)=0.0;  
			 else
				r(j)=u(lm(i,j));
			endif;
		endfor;

		endForces = beam2d_postpro(xz(i,:), EA(secchar(i)), EI(secchar(i)), r);
		
		i
		eFor = -endForces;
		
		flok = beam2d_load(xz(i,:), 0., load(i,2));
		
		eFor = eFor + flok;
		
		eFor(3,1) = -eFor(3,1);
		eFor(4,1) = -eFor(4,1);
		eFor(5,1) = -eFor(5,1)

		eForces(i,:) = eFor(:);
		
		if load(i, 2) != 0.
			if (eFor(2) < 0. && eFor(5) > 0) || (eFor(2) > 0. && eFor(5) < 0)
				x = abs(eFor(2)) * length(xz(i,:)) / (abs(eFor(2)) + abs(eFor(5)))
				M = eFor(3) + load(i,2) * x * x / 2 - eFor(2) * x
				d = 0;
			else
				if abs(eFor(3)) > abs(eFor(6))
					x = 0.;
					M = abs(eFor(3));
					d = 1;
				else
					x = length(xz(i,:));
					M = abs(eFor(6));
					d = 2;
				endif;
			endif;
		else
			if abs(eFor(3)) > abs(eFor(6))
					x = 0.;
					M = abs(eFor(3));
					d = 1;
				else
					x = length(xz(i,:));
					M = abs(eFor(6));
					d = 2;
			endif;
		endif;
		
		%if n == 0
			p(i) = Mpl(secchar(i))/M
		%else
			%p(i) = (Mpl(secchar(i))-Mmax(i,1)*P(n))/M
		%endif;
		
		Mmax(i,1) = M;
		Mmax(i,2) = x;
		Mmax(i,3) = d;
		
		%Mmax_1(i,n+1) = M;
		
	endfor;

	eForces
	Mmax

	p

	"sorted p:"
	
	[p,e] = sort(p)
	
	P = p(1)
	
%endfor;

neq = neq+1;
popis = resize(popis, neq, 2);
k = zeros(neq);
f = zeros(neq,1);

if Mmax(e(1),3) == 1;
	popis(neq,1) = popis(lm(e(1),3),1);
	lm(e(1),3) = neq;
else
	popis(neq,1) = popis(lm(e(1),6),1);
	lm(e(1),6) = neq;
endif;

popis(neq,2) = "4"

for i=1:nelem;
	kel = beam2d_stiffness(xz(i,:), EA(secchar(i)), EI(secchar(i)));
	k = assembly(k, kel, i);
endfor;

for i=1:nelem;
	flok = beam2d_load(xz(i,:), load(i,1), load(i,2));
	f = assemblyf(f, flok, lm, i);
endfor;

f(4,1) = f(4,1) + 20000. * c;
f(11,1) = f(11,1) + 2000. * a;

u=k\f;

for i=1:neq;
	popis(i,:)
	i;
	u(i)
endfor;

for i=1:nelem;
	r=zeros(6,1);
	for j=1:6;
		 if lm(i,j) == 0
			 r(j)=0.0;  
		 else
			r(j)=u(lm(i,j));
		endif;
	endfor;

	endForces = beam2d_postpro(xz(i,:), EA(secchar(i)), EI(secchar(i)), r);
	
	i
	eFor = -endForces;
	
	flok = beam2d_load(xz(i,:), 0., load(i,2));
	
	eFor = eFor + flok;
	
	eFor(3,1) = -eFor(3,1);
	eFor(4,1) = -eFor(4,1);
	eFor(5,1) = -eFor(5,1)

	eForces(i,:) = eFor(:);
	
	if load(i, 2) != 0.
		if (eFor(2) < 0. && eFor(5) > 0) || (eFor(2) > 0. && eFor(5) < 0)
			x = abs(eFor(2)) * length(xz(i,:)) / (abs(eFor(2)) + abs(eFor(5)))
			M = eFor(3) + load(i,2) * x * x / 2 - eFor(2) * x
			d = 0;
		else
			if abs(eFor(3)) > abs(eFor(6))
				x = 0.;
				M = abs(eFor(3));
				d = 1;
			else
				x = length(xz(i,:));
				M = abs(eFor(6));
				d = 2;
			endif;
		endif;
	else
		if abs(eFor(3)) > abs(eFor(6))
				x = 0.;
				M = abs(eFor(3));
				d = 1;
			else
				x = length(xz(i,:));
				M = abs(eFor(6));
				d = 2;
		endif;
	endif;
	
	%if n == 0
		p(i) = (Mpl(secchar(i)) - Mmax(i,1)*P)/M
	%else
		%p(i) = (Mpl(secchar(i))-Mmax(i,1)*P(n))/M
	%endif;
	
	Mmax(i,1) = M;
	Mmax(i,2) = x;
	Mmax(i,3) = d;
	
	%Mmax_1(i,n+1) = M;
	
endfor;

eForces
Mmax

p

"sorted p:"

[p,e] = sort(p)

neq = neq+1;
popis = resize(popis, neq, 2);
k = zeros(neq);
f = zeros(neq,1);

	popis(neq,:) = "b3";
	lm(e(1),3) = neq;

for i=1:nelem;
	kel = beam2d_stiffness(xz(i,:), EA(secchar(i)), EI(secchar(i)));
	k = assembly(k, kel, i);
endfor;

for i=1:nelem;
	flok = beam2d_load(xz(i,:), load(i,1), load(i,2));
	f = assemblyf(f, flok, lm, i);
endfor;

f(4,1) = f(4,1) + 20000. * c;
f(11,1) = f(11,1) + 2000. * a;

u=k\f;

for i=1:neq;
	popis(i,:)
	i;
	u(i)
endfor;

for i=1:nelem;
	r=zeros(6,1);
	for j=1:6;
		 if lm(i,j) == 0
			 r(j)=0.0;  
		 else
			r(j)=u(lm(i,j));
		endif;
	endfor;

	endForces = beam2d_postpro(xz(i,:), EA(secchar(i)), EI(secchar(i)), r);
	
	i
	eFor = -endForces;
	
	flok = beam2d_load(xz(i,:), 0., load(i,2));
	
	eFor = eFor + flok;
	
	eFor(3,1) = -eFor(3,1);
	eFor(4,1) = -eFor(4,1);
	eFor(5,1) = -eFor(5,1)

	eForces(i,:) = eFor(:);

#{	
	if load(i, 2) != 0.
		if (eFor(2) < 0. && eFor(5) > 0) || (eFor(2) > 0. && eFor(5) < 0)
			x = abs(eFor(2)) * length(xz(i,:)) / (abs(eFor(2)) + abs(eFor(5)))
			M = eFor(3) + load(i,2) * x * x / 2 - eFor(2) * x
			d = 0;
		else
			if abs(eFor(3)) > abs(eFor(6))
				x = 0.;
				M = abs(eFor(3));
				d = 1;
			else
				x = length(xz(i,:));
				M = abs(eFor(6));
				d = 2;
			endif;
		endif;
	else
		if abs(eFor(3)) > abs(eFor(6))
				x = 0.;
				M = abs(eFor(3));
				d = 1;
			else
				x = length(xz(i,:));
				M = abs(eFor(6));
				d = 2;
		endif;
	endif;
	
	%if n == 0
		p(i) = (Mpl(secchar(i)) - Mmax(i,1)*P)/M
	%else
		%p(i) = (Mpl(secchar(i))-Mmax(i,1)*P(n))/M
	%endif;
	
	Mmax(i,1) = M;
	Mmax(i,2) = x;
	Mmax(i,3) = d;
	
	%Mmax_1(i,n+1) = M;
	
#}
	
endfor;

eForces
%Mmax

%p

%"sorted p:"

%[p,e] = sort(p)
