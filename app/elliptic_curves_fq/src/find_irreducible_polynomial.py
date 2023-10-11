from .endlicheKoerper_Fp import Fp
from .endlicherKoerper_Fpn import Fpn
import copy
import random


def gcd_is_linear(f,Poly):
    a = copy.copy(f)
    b= Poly.value
    while sum(b)!= 0:
        division = Poly.div(a,b)
        while len(division[1])!= 0:
            if division[1][0] == 0:
                division[1].pop(0)
            else: break            
        a = b
        b = division[1]
        #print(division)
    while len(a) != 0:
        if a[0] == 0:
            a.pop(0)
        else: break
    if len(a) != 1:
        return False
    else: 
        return True

def is_irreductible(p, f):
    degree = len(f)-1
    d = degree // 2 
    Poly = Fpn(p,f,[1,0])
    for i in range(1, d+1):
        Poly = Poly**p
        if gcd_is_linear(f,Poly-[1,0]):
            continue
        else:
            return(False)
    return True       
def get_irreductible_polynomial(p,n):
    a=0
    while True:
        a+=1
        Poly =[1]
        for i in range(n):
            Poly += [random.randrange(p)]
        if is_irreductible(p,Poly):
            return Poly,a
        