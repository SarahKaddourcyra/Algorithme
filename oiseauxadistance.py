# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:25:08 2020

@author: sarah
"""

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
#import numpy as np
import math
import time
from plot import plot
poids = []
y = []
with open('./data/ulysses16.tsp') as f:
        for line in f.readlines():
            #print(line)
            city = line.split(' ')
            #print(city)
            poids.append(float(city[1]))
            y.append(float(city[2]))
n=len(poids)
nbr_ois=10000
#f=[0]*n
#F=[0]*n
#print(n)
def __prodx(x=[]):
    for i in range(nbr_ois):
        a=[]
        while (len(a)!=n):
            b=(random.randint(0, n-1))
            if(a.count(b)==0):
                a.append(b)
        x.append(a)
    return(x)
    
def __vol(x_prim=[]):
    while (len(x_prim)!=n):  #la taill de x' egal au nombre de villes(la taille de nbr_villes)
        a=random.randint(0,n-1)#générer x' hoasard en utulisons random
        b=x_prim.count(a) 
        if b==0:
            x_prim.append(a)
        
    return (x_prim)
def __marche(i,x):
    #print(x)
    delta=0
    while(delta<=1):
       j=random.randint(0,nbr_ois-1)
       while(j==i):
           j=random.randint(0,nbr_ois-1)
       k=random.randint(1,n-1)
       #print('k et j',k,j)
       delta=math.fabs(x[j].index(x[i][k])-x[j].index(x[i][k-1]))
    l=(k+int(delta)) %(n)
   # print(l,k,delta)
    if(k>l):
       c=k
       k=l
       l=c
    x_prim=x[i]
    #print(x_prim)
    #print(k,l)
    c=[]
    for i in range(k,l+1):
       c.append(x_prim[i])   
    c.reverse()
    #print(c)
    m=0
    for i in range(k,l+1):
       x_prim[i]=c[m]
       m=m+1
    return( x_prim)

def __nbroiseauartificiel(nbr_ois,f,F,X=[],d=[]):
   x=__prodx(x=[])
   #X=[]
   #print(nbr_ois)
   
   for i in range(nbr_ois): 
      #print(F[i])
      a=__vol(x_prim=[])
      x[i]=a
      X.append(a)
      d.append(2)
      F[i]=__calculcout(x,i)
      f[i]=F[i]
   return(x,X,F,f,d)
def __lesproba():
    p_2=random.random()
    p_3=random.random()
    p_4=random.random()
    return(p_2,p_3,p_4)
def __calculcout(x,i):
    #F=F*n
    #print(x)
    s=0
    for m in range(n-1):
       #print('la somme 1',s)
       s=s+math.sqrt((poids[x[i][m]]-poids[x[i][m+1]])**2+(y[x[i][m]]-y[x[i][m+1]])**2)
       #print('la somme 2',s)
            #print('les poids',poids[x[i][m]][x[i][m+1]])
    #print(x[i][0],x[i][-1])  
       
    s=s+math.sqrt((poids[x[i][0]]-poids[x[i][-1]])**2+(y[x[i][0]]-y[x[i][-1]])**2)
    return(s)
debut=time.time()
F_k=[]
F_km=[]
X_k=[]
X_kk=[]
ta=0
while(ta<1):
 print('sinarieu',ta+1)
 p_2,p_3,p_4=__lesproba()
 f=[0]*nbr_ois
 F=[0]*nbr_ois
 x,X,F,f,d=__nbroiseauartificiel(nbr_ois,f,F,X=[],d=[])
 #print(f)
 #print(x)
 t=0
 while(t<2):
      p_2,p_3,p_4=__lesproba()
      for i in range(nbr_ois): 
        #print(d)
        if (d[i]==2 | d[i]==3 | d[i]==4 | int(f[i])==int(F[i])):
            p=1
            #print('1')
        else:
            p=random.random()
            #print('2')
        if (p>(p_2+p_3+p_4)):
            d[i]=1
            x[i]=__marche(i,x)
            f[i]=__calculcout(x,i)
            #print('3')
        elif(p<p_2):
            d[i]=2
            x[i]=__vol(x_prim=[])
            f[i]=__calculcout(x,i)
        elif(p<(p_2+p_3)):
            d[i]=3
            v=random.randint(0,nbr_ois-1)
            x[i]=x[v]
            f[i]=__calculcout(x,v)
            #print('5')
        else:
            d[i]=4
            x[i]=X[i]
            f[i]=F[i]
           # print('6')
        if(f[i] <= F[i]):
            X[i]=x[i]
            F[i]=f[i]
      t=t+1
 b=min(F)
 F_k.append(min(F))
 F_km.append(max(F))
 #print('le max et le min',F_k,F_km)
 a=F.index(b)
 X_k.append(X[a])
 #print(X_k)
 ta=ta+1
#print(F_k) 
F_kkm=(max(F_k)) 
F_kk=(min(F_k))
a=F_k.index(F_kk)
X_kk=X_k[a]
#print(X_kk) 
for i in range(n):
    X_kk[i]=X_kk[i]+1 

fin=time.time() 
#print(x,f,F,X)
#print('le max %d et le min %d',ù(F_kkm,F_kk))
print ('Solution finale par l algorithme des oiseaux picorant artificiels(OPA):\n %s | le coût: %f\n' % (' -> '.join(str(i) for i in X_kk),F_kk))
print('terminer le temps dexecution=',fin-debut)
#del(X_kk[-1])
for i in range(len(X_kk)):
   X_kk[i]=X_kk[i]-1
X_kk.append(X_kk[0])
x=[]
y=[]
points=[]
with open('./data/ulysses16.tsp') as f:
           for line in f.readlines():
             #print(line)
             city = line.split(' ')
             #print(city)
             x.append(float(city[1]))
             y.append(float(city[2]))
             points.append((float(city[1]), float(city[2])))
plot(points,X_kk)


        
                
        
            
            
            
            
    

    