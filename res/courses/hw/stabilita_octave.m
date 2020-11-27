%
% stabilita rámu

% pole kodovych cisel
global koef = [ 1.2, 0.8, 0.7 ];
global nelemstruts = 5;

a= 5 + koef(1);
b= 3 + koef(1);
c= 2 + koef(2);

% jednotlive prvky, cisla koncovych uzlu
nstruts = 15;
struts = [ 1, 4;
			2, 5;
			3, 6;
			4, 7;
			5, 8;
			6, 9;
			7, 10;
			8, 11;
			9, 12;
			4, 5;
			5, 6;
			7, 8;
			8, 9;
			10, 11;
			11, 12];

% souradnice koncovych uzlu [x,z] [m]	
nodes = [ 0, 0;
			a, 0;
			2*a, 0;
			0, c;
			a, c;
			a+b, c;
			0, 2*c;
			a, 2*c;
			a+b, 2*c;
			0, 3*c;
			a, 3*c;
			a+b, 3*c];
			
% prurezove charakteristiky [E = Pa, A = m2, I = m4]
E = 25e9;
A_s = 0.3 * (0.3 + 0.1 * koef(2));
I_s = 1/12 * 0.3 * (0.3 + 0.1 * koef(2))^3;
A_p = 0.3 * (0.4 + 0.1 * koef(1));
I_p = 1/12 * 0.3 * (0.4 + 0.1 * koef(1))^3;

% deleni prutu na elementy
nelem = nstruts * (nelemstruts + 1);
xz = zeros(nelem, 2 );
for i = 1: nstruts
	for j = 1:(nelemstruts + 1)
		xz((i-1)*(nelemstruts + 1) + j, 1) = (nodes(struts(i,1),1) + (j-1) * (nodes(struts(i, 2),1) - nodes(struts(i,1),1))/nelemstruts;
		xz((i-1)*(nelemstruts + 1) + j, 2) = (nodes(struts(i,1),2) + (j-1) * (nodes(struts(i,2),2) - nodes(struts(i, 1),2))/nelemstruts;
	endfor
endfor


% global lm = zeros(  15*(nelemstrut+1), 6)
% for i= 1:nelem
	% for j = 1:6
		% lm(i, j) = i + j
	% endfor
% endfor