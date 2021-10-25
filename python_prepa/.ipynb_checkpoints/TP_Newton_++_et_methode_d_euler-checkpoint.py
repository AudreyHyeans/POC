--import matplotlib as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def Newton (x0,P,Pp,N):
    x=x0
    p=x0-P(x)/Pp(x)
    while abs(x-p)=10**(-4):
        x=p
        if Pp(x)=0:
            return(N)
        p=p-P(p)/Pp(p)
        M=M+1
        if M>N:
            return(p)
    return(x,M)   
    
def P(A,x):
    y=x**3-Ax**2+Ax-1
    return(y)

def Pp(A,x):
    y=3x**2-2Ax+A
    return(y)
    

    
    
    
            
        