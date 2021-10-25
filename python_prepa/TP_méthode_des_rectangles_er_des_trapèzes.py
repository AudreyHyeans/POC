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
  
    
        
    
    