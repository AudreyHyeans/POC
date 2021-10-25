def MethodeRectangles(a,b,f,n):
    S=0
    h=(b-a)/n
    for i in range (0,n):
        S=S+h*f(a+i*h)
    return S
    
def MethodeTrapezes(a,b,f,n):
    S=0
    h=(b-a)/(n)
    for i in range (0,n):
        S=S+(h*(f(a+i*h)+f(a+(i+1)*h)))/2
    return(S)
    
def F(x):
    y=4/(1+x**2)
    return (y)
    
x=MethodeTrapezes(0,1,F,1000)
print(x)  

import numpy as np
import matplotlib.pyplot as plt

def CompareMethodes(epsilon):
    g=lambda x : 1/np.sqrt((1+x**2))
    R=MethodeRectangles(0,1,g,1)
    T=MethodeTrapezes(0,1,g,1)
    N1=1
    N2=1
    while abs(R-np.arcsinh(1))>epsilon:
        R=MethodeRectangles(0,1,g,N1+1)
        N1=N1+1
    while abs (T-np.arcsinh(1))>epsilon:
        T=MethodeTrapezes(0,1,g,N2+1)
        N2=N2+1
    return[N1,N2]
    
a=CompareMethodes (0.01)
print (a)

def TraceComparaison (n,N):
    L1=[]
    L2=[]
    X=[ i for i in range (1,1001)]
    for i in range (1,1001):
        e=10**(-N)-i*((10**(-N)-10**(-n))/1000)
        print("e",e)
        a=CompareMethodes(e)
        L1=L1+[a[0]]
        L2=L2+[a[1]]
    plt.plot(X,L1)
    plt.plot(X,L2)
TraceComparaison(3,2)


        

  
    
        
    
    