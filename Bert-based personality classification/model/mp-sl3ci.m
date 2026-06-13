clc;clear;close all;

C = csvread('event.csv');
C_F1= C(1:end,2);
C_F2= C(1:end,3);
C_F3= C(1:end,4);
C_F4= C(1:end,5);
C_F5= C(1:end,6);
C_F6= C(1:end,7);

L=length(C_F1);
d=0:(L-1);

F10=C_F1(1);    %dy-e
F20=C_F2(1);    %dy-r
F30=C_F3(1);    %dy-a
F40=C_F4(1);    %wb-e
F50=C_F5(1);    %wb-r
F60=C_F6(1);    %wb-a
          
C_F10=C_F1(1);   
C_F20=C_F2(1);  
C_F30=C_F3(1);  
C_F40=C_F4(1);    
C_F50=C_F5(1);    
C_F60=C_F6(1);    

f=0.1;                                                                        
figure('units','normalized','position',[0,0,0.4,0.5],'Color',[1 1 1])         
figure(1)

lamede=
lamede1=
q=
q1=
m1=
m2=
m3=
m4=
m5=
m6=
beta=
beta1=
y1=
y2=
x3=
y3=
xita1=
xita2=
xita3=
xita4=
xita5=
xita6=
a1=
a2=
a3=
a4=
a5=
a6=
b1=
b2=
b3=
b4=
b5=
b6=

S10=
S20=
L10=0
L20=0
I10=0
I20=0

parameters=[lamede,b6,lamede1,q,q1,x3,y3,y1,y2,beta,beta1,m1,m2,m3,m4,m5,m6,xita1,xita2,xita3,xita4,xita5,xita6,a1,a2,a3,a4,a5,a6,b1,b2,b3,b4,b5];
X0=[S10,S20,L10,L20,F10,F20,F30,F40,F50,F60,I10,I20,C_F10,C_F20,C_F30,C_F40,C_F50,C_F60];
options = odeset('RelTol',1e-2,'AbsTol',1e-7);
[T,X]=ode45(@(t,y) Srgmodel(t,y,parameters),[],X0,options);    

colorstr1='#E2A6A6';
colorstr2='#E46464';
colorstr3='#A78540';
colorstr4='#F79F1C';
colorstr5='#A2BB8B';
colorstr6='#598532';
colorstr7='#59B0B5';
colorstr8='#224244';
colorstr9='#51B6FA';
colorstr10='#0434B8';
colorstr11='#A0A0D7';
colorstr12='#821E81';
color1 = sscanf(colorstr1(2:end),'%2x%2x%2x',[1 3])/255;
color2 = sscanf(colorstr2(2:end),'%2x%2x%2x',[1 3])/255;
color3 = sscanf(colorstr3(2:end),'%2x%2x%2x',[1 3])/255;
color4 = sscanf(colorstr4(2:end),'%2x%2x%2x',[1 3])/255;
color5 = sscanf(colorstr5(2:end),'%2x%2x%2x',[1 3])/255;
color6 = sscanf(colorstr6(2:end),'%2x%2x%2x',[1 3])/255;
color7 = sscanf(colorstr7(2:end),'%2x%2x%2x',[1 3])/255;
color8 = sscanf(colorstr8(2:end),'%2x%2x%2x',[1 3])/255;
color9 = sscanf(colorstr9(2:end),'%2x%2x%2x',[1 3])/255;
color10 = sscanf(colorstr10(2:end),'%2x%2x%2x',[1 3])/255;
color11 = sscanf(colorstr11(2:end),'%2x%2x%2x',[1 3])/255;
color12 = sscanf(colorstr12(2:end),'%2x%2x%2x',[1 3])/255;

%C_F1
p1=plot(d,C_F1(d+1),'*','color',color1);hold on;     %real
p2=plot(T,X(:,13),'-','linewidth',1.5,'color',color2);hold on;    %fitting

p5=plot(d,C_F2(d+1),'*','color',color3);hold on;
p6=plot(T,X(:,14),'-','linewidth',1.5,'color',color4);hold on;

p9=plot(d,C_F3(d+1),'*','color',color5);hold on;
p10=plot(T,X(:,15),'-','linewidth',1.5,'color',color6);hold on;

p3=plot(d,C_F4(d+1),'*','color',color7);hold on;
p4=plot(T,X(:,16),'-','linewidth',1.5,'color',color8);hold on;

p7=plot(d,C_F5(d+1),'*','color',color9);hold on;
p8=plot(T,X(:,17),'-','linewidth',1.5,'color',color10);hold on;

p11=plot(d,C_F6(d+1),'*','color',color11);hold on;
p12=plot(T,X(:,18),'-','linewidth',1.5,'color',color12);hold on;

h=legend([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12],'real {\itC_{{\itC}_{\itE}^{\iti}}}','estimate {\itC_{{\itC}_{\itE}^{\iti}}}','real {\itC_{{\itC}_{\itE}^{\itj}}}','estimate {\itC_{{\itC}_{\itE}^{\itj}}}','real {\itC_{{\itC}_{\itR}^{\iti}}}','estimate {\itC_{{\itC}_{\itR}^{\iti}}}','real {\itC_{{\itC}_{\itR}^{\itj}}}','estimate {\itC_{{\itC}_{\itR}^{\itj}}}','real {\itC_{{\itC}_{\itA}^{\iti}}}','estimate {\itC_{{\itC}_{\itA}^{\iti}}}','real {\itC_{{\itC}_{\itA}^{\itj}}}','estimate {\itC_{{\itC}_{\itA}^{\itj}}}');
set(h,'FontName','Times New Roman','FontSize',10)
hold on ;
xlabel('t','FontName','Times New Roman','FontSize',12);ylabel('n','FontName','Times New Roman','FontSize',22);xlim([0,50]);ylim([0,17000])



