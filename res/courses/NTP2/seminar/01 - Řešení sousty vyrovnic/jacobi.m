%Jacobi 

A = [1 -1 0;-1 2 -1;0 -1 2]
b = [1;0;0]

% spravne reseni
r =A\b

D_vect = diag(A);
D_inv = 1./D_vect;

D_1 = diag(D_inv);%diagonal
E = -tril(A,-1);%lower
F = -triu(A,1);%upper

x = [1;1;1]
    
for c=1:100
   
%Jacobi
t = D_1*(E+F)*x + D_1*b
x=t;
%residuum
residuum = A*x - b;

end


