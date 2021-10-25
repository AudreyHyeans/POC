# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import matplotlib.pyplot as plt
import random as rd
import time

def TriInsertion(L):
    for i in range(len(L)):
        a = L[i]
        rg = i
        while L[rg-1] > a and rg > 0:
            L[rg] = L[rg - 1]
            rg = rg - 1
        L[rg] = a
    return(L)
    

Ltailles = [10+k*10 for k in range(0,101)] 
Ltemps = []
Ltemps2 =  []
for taille in Ltailles:
    L = [rd.randint(1,100) for i in range(0,taille)]  
    M = [L[i] for i in range(len(L))]
    t0 = time.time()
    TriInsertion(L)
    t1 = time.time()
    M.sort
    t2 = time.time()
    Ltemps = Ltemps + [t1-t0]
    Ltemps2 = Ltemps2 + [t2-t1]
plt.plot(Ltailles, Ltemps,"k")
plt.plot(Ltailles, Ltemps2,"r")
print(t0,t1,t2)

    
def NouveauRang(L,i):
    nbElemAvant = 0
    nbElemApres = 0
    for k in range(0,i):
        if L[k] <= L[i]:
            nbElemAvant = nbElemAvant + 1
    for k in range(i+1, len(L)):
        if L[k] < L[i]:
            nbElemApres = nbElemApres + 1
    return(nbElemAvant + nbElemApres)     
    
def ListeRangs(L):
    M = [0]*len(L)
    for i in range(len(L)):
        M[i] = NouveauRang(L,i)
    return(M)

def ReconstruitListe(L,R):
    M = [0] * len(L)
    for k in range(len(L)):
        M[R[k]] = L[k] 
    return(M)



        









        