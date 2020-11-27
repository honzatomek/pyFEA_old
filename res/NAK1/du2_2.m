a=1.2;
b=0.8;
c=0.7;

nnode=8;
nelem=7;
neq=19;

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


	