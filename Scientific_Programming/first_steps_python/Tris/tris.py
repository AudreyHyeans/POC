import random

def TriaBulles(L):
    Ech = True
    while Ech:
        Ech = False
        for i in range(len(L)-1):
            if L[i] > L[i+1]:
                L[i],L[i+1] = L[i+1],L[i]
                Ech = True

    return(L)


def TriInsertion(L):
    for i in range(1,len(L)):
        rg = i
        while L[rg-1] > L[i] and rg > 0 :
            L[rg] = L[rg -1]
            rg = rg - 1
        L[rg] = L[i]

    return(L)



L = [random.randrange(0,100) for i in range(10)]
print(L)