# fichier somme.py
###################################
# Programme Python type : somme.py
###################################
###################################
# Importation des fonctions externes
from math import pow
###################################
# Definition locale des fonctions
def factorielle(n):
#""" Calcule la factorielle de n """
# ces commentaires decrivent fonction et argument
    f = 1
    for i in range(1,n+1):
        f = f * i
    return f

def k_parmi_n(k,n):
#""" Calcule le coefficient binomiaux k parmi n """
    c = factorielle(n)/( factorielle(k)*factorielle(n-k) )
 # fonction factorielle appelee
    return c
def somme(x,n,verbose=False):
#""" Calcule la somme des k parmi n fois x exposant k """
    s = 0
    for k in range(n+1):
        s = s + k_parmi_n(k,n) * pow(x,k)
 # appelle k_parmi_n qui appelle factorielle

    if verbose :
        print('k =',k,': s =',s)
    if verbose :
        print('La somme pour n =',n,' et x =',x,'vaut',s)
    return s

def test_somme(x,n,verbose=False):
#""" Teste l’egalite de l’enonce """
    test = False
    polynom = pow((1+x),n)
    s = somme(x,n,verbose)
    if s == polynom :
        test = True
        if verbose :
            print ('Egalite OK')
    else :
        if verbose :
            print ('Egalite non verifiee')
    return test
###################################
# Corps principal du programme

#if __name__ == "__main__":
test_somme(x=2,n=5,verbose=True)
