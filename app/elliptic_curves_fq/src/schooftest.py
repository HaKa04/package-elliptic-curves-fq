'Schoof algorithmus, um Ordung der Elliptischen Kurve zu bestimmen'
from .Kurven import ord353
from .elliptischeKurve import on_Curve
from .endlicherKoerper_Fpn import Fpn
import math
import copy
from .ChinesischerRestsatz import solve_for_a
class Polynom:
    ' Klasse eines Polynom mit Koeffizienten in F(p^n)'
    def __init__(self,value, Curve):
        if isinstance(value[0],list):
            self.value = [Fpn(Curve.a.p,Curve.a.ir_poly,value[i]) for i in range(len(value))]
        else: self.value = value
        self.Curve = Curve
    def __str__(self):
        L = []
        for i in self.value:
            L.append(i.value)
            return (str(L))
    def __mul__(self,other):
        n = len(self.value)
        result = [Fpn(self.Curve.a.p, self.Curve.a.ir_poly,[0]) for _ in range(2 * n - 1)]
        for i in range(n):
            for j in range(n):
                result[i+j] += self.value[i] * other.value[j]
        return (Polynom(result,self.Curve))
    def __mod__(self,other):
        if (len(self.value) == 5):
            otherlist = [[1],[0]]
            Curvemod =  [Fpn(other.a.p,other.a.ir_poly,otherlist[i]) for i in range(2)] + [other.a, other.b]
            value = copy.copy(self.value)
            while len(value) >= len(Curvemod):  
                first_of_mod = value[0]
                facter = first_of_mod.invminus() / Curvemod[0]
                #print(value,"--", facter, "--", Curvemod)
                for i in range(4):
                    value[i] = ( value[i]  + (facter * Curvemod[i]))
                value = value[1:]
            return(Polynom(value,self.Curve))
        else:
            if other.sum() == 0:
                print("division by Zero")
                return None
            while len(other.value)!= 0:
                    if sum(other.value[0].value) == 0:
                        other.value.pop(0)
                    else: break
            while len(self.value)>= len(other.value):
                    if sum(self.value[0].value) == 0:
                        self.value.pop(0)
                    else: break
            degree = len(other.value) - 1
            if len(self.value) < len(other.value):
                return ([0], value)
            while len(self.value) >= degree + 1:
                if sum(self.value[0].value) == 0:
                    self.value = self.value[1:]

                else:
                    first_of_mod = self.value[0]
                    facter = first_of_mod.invminus() / other.value[0]
                    for i in range(degree + 1):
                        self.value[i] = ( self.value[i]  + (facter * other.value[i]))
                    self.value = self.value[1:]
            return(Polynom(self.value,self.Curve))
    def sum(self):
        Summe =0
        for i in self.value:
            Summe +=sum(i.value)
        return (Summe)



def remainderT2(Curve): 
    'calculate ggt((x^q-x),x^3+ax+b)'
    q = Curve.a.q
    a = Curve.a
    b = Curve.b
    xDynamisch = Polynom([[0],[1],[0]], Curve)
    Modulos = Polynom([[0],[0],[1]], Curve)
    #print("mod",Modulos.value,"Dyn", xDynamisch.value,q)
    while q > 0:
        if q % 2 == 1: Modulos = (Modulos * xDynamisch) % Curve
        xDynamisch = (xDynamisch * xDynamisch) % Curve
        q = q // 2
        #print("mod",Modulos.value,"Dyn", xDynamisch.value ,q)
    Modulos.value[-2] -= Fpn(Modulos.value[-2].p,Modulos.value[-2].ir_poly,[1])
    #print("--------")
    if Modulos.sum() == 0:
        return 0
    else:
        otherlist = [[1],[0]]
        fx = Polynom([Fpn(Curve.a.p,Curve.a.ir_poly,otherlist[i]) for i in range(2)] + [Curve.a, Curve.b], Curve)
        b = Modulos
        #print(fx.value," % ", b.value, " = :")
        temp = fx % b
        #print(temp.value )
        if temp.sum()== 0:
            return ((Polynom (b.value[0:-2], Curve).sum() != 0))
        else:
            #print(b.value," % ",temp.value, " = :")
            final = b % temp
            #print(final.value)
            if final.sum()== 0:
                return (int(sum(temp.value[0].value) == 0))
            else: return 1


        
    


def remainderTl(Curve,l):
    'calculate remainder t mod l'
    q = Curve.a.q
    a = Curve.a
    b = Curve.b
    q_mod_l = q % l
    if q_mod_l > l / 2 :
        q_mod_l -= l









    if l == 3 : return 0
    if l == 5: return 1
    if l == 7: return 5
    return 1


def main_schoof(Curve):
    q = Curve.a.q
    
    List_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 
                   137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 
                   277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 
                   439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 
                   607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 
                   773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 
                   967, 971, 977, 983, 991, 997]
    Tl = []
    Tl.append(remainderT2(Curve))
    count = 1
    primecount = 2
    Hasse = math.ceil(4* math.sqrt(q))
    while primecount < Hasse:
        
        primecount *= List_primes[count]
        Tl.append(remainderTl(Curve,List_primes[count]))  
        count += 1
        
    t = solve_for_a(List_primes[0:count],Tl)
    if t > 2 * math.sqrt(q):
        t = t - primecount
    print(primecount)
    return [[q,t], (q + 1 - t), Tl]

test = ord353()
print(test.discriminante_is_zero())
a = main_schoof (test)
print(a)

Point=test.startpoint
print(Point)
if on_Curve(Point, test):
    Point *= a[1]
    print(Point)
else: print( "not on Curve")