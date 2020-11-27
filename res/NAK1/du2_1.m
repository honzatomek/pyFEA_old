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

As = bs * hs;
Ap = bp * hp;

Is = 1/12 * bs * hs * hs * hs;
Ip = 1/12 * bp * hp * hp * hp;				

EA = zeros(2,1);
EI = zeros(2,1);
Mpl = zeros(2,1);

EA(1) = E * As;
EI(1) = E * Is;
EA(2) = E * Ap;
EI(2) = E * Ip;

Mpl(1) = 100000. + (20000. * c);
Mpl(2) = (1. + c) * Mpl(1);

f(4,1) = 20000. * c;
f(11,1) = 2000. * a;
	
	flok = zeros(6,1);
	f=zeros(neq,1);
	k=zeros(neq);
	kel=zeros(6);
	r=zeros(6,1);

	for i=1:nelem;
		flok = beam2d_load(xz(i,:), 0., load(i,2));
		f = assemblyf (f, flok, lm, i);
	endfor;

	for i=1:nelem;
	 kel=beam2d_stiffness(xz(i,:), EA(secchar(i),1), EI(secchar(i),1));
	 k=assembly(k,kel,i);
	endfor;

	u=k\f;

	for i=1:neq;
		popis(i,:)
		i;
		u(i)
	endfor;

	p = zeros(nelem,1);
	Mmax = zeros(nelem, 3);
	eForces = zeros(nelem, 6);
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

		endForces = beam2d_postpro(xz(i,:), EA(secchar(i),1), EI(secchar(i),1), r);
		
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
		

		p(i) = Mpl(secchar(i))/M;

		Mmax(i,1) = M;
		Mmax(i,2) = x;
		Mmax(i,3) = d;
		
	endfor;

	eForces
	Mmax;

	p;

	"sorted p:"
	
	[p,e] = sort(p);

	
%endfor;
