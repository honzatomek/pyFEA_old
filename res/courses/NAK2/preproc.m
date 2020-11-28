% Preprocess vstupnich dat
%
% Input:
% nnode - pocet uzlu
% ndof  - pocet stupnu volnosti v uzlech
% nelem - pocet prvku
% nelnode pocet uzlu definujicich prvek
% bc - pole kodovych cisel uzlu (0 - nepodepreno, 1-n podepreno + cislo bc)
% 
% Output:
% id - pole kodovych cisel uzlu, cislovany predepsane i nezname posuny
%      (predepsane posuny cislovany v rozsahu 1..pneq, 
%      dale nezname v rozsahu pneq+1..neq)
% lm - pole kodovych cisel prvku (element_index, code_number_index)
%
% (c) Borek Patzak

function preproc;

global bc;
global id;
global nnode;
global nelem;
global ndof;
global uneq; 
global pneq; 
global neq;
global lm;
global elnode;
global nelnode;

%count number of prescribed (pneq) and number of unknowns (neq)
uneq = 0; % pocet neznamych posunu
pneq = 0; % pocet predepsanych posunu
for i=1:nnode
 for j=1:ndof
   if bc(i,j) > 0 
     pneq=pneq+1;
   else
     uneq = uneq+1;
   end
  end
end

neq=uneq+pneq;

%number equations
countp=0; count=pneq;
for i=1:nnode
  for j=1:ndof
    if bc(i,j)>0
      countp=countp+1;
      id (i,j)=countp;
    else
      count=count+1;
      id (i,j)=count;
    end
  end
end

%assemble element lm array (element code numbers)
for i=1:nelem
 c=1;
 for j=1:nelnode
  lm(i,c:c+ndof-1) = id (elnode(i,j),:);
  c=c+ndof;
 end
end
