from .fast_curve import fast_F47_hoch_48
import numpy as np
from itertools import zip_longest

class Polynomial:
    ' Klasse eines Polynom mit Koeffizienten in F(p^n)'
    def __init__(self,value):
        if isinstance(value[0],np.ndarray):
            self.value = [fast_F47_hoch_48(value[i]) for i in range(len(value))]
        else: self.value = value
        self.p = 47
    def __str__(self):
        L = []
        for i in self.value:
            L.append(i.value)
        return (str(L))
    
    def __repr__(self):
        L=[]
        for i in self.value:
            L.append(i.value)
        return (str(L))

    def __mul__(self, other):
        
        result = karatsuba_mul(self.value, other.value)
        return Polynomial(result)
    
    def __truediv__(self,other):
        if other == 2:
            self.value = [i * 24 for i in self.value]
            return (self)

    def sum(self):
        Summe =0
        for i in self.value:
            Summe +=sum(i.value)
        return (Summe)
    
    def __sub__(self,other):
        if len(self.value) < len(other.value):
            self.value = [fast_F47_hoch_48(np.zeros(48,dtype=int)) for _ in range(len(other.value) - len(self.value))] + self.value
        elif len(self.value) > len(other.value):
            other.value = [fast_F47_hoch_48(np.zeros(48,dtype=int)) for _ in range(len(self.value) - len(other.value))] + other.value
        result = [self.value[i] - other.value[i] for i in range(len(self.value))]
        return Polynomial(result)


class Division_Polynomial():

    def __init__(self, a, b, h=[0,0]):
        self.a = a
        self.b = b
        self.h = h

    def get_division_polynomial(self, l):
        Phi0 = Division_Polynomial(self.a, self.b ,[0, Polynomial([np.zeros(48, dtype=int)])])
        Phi1 = Division_Polynomial(self.a, self.b, [0, Polynomial([np.concatenate((np.zeros(47, dtype=int), [1]))])])
        Phi2 = Division_Polynomial(self.a, self.b, [1, Polynomial([np.concatenate((np.zeros(47, dtype=int), [2]))])])
        Phi3 = Division_Polynomial(self.a, self.b, [0, Polynomial([np.concatenate((np.zeros(47, dtype=int), [3])),
                                                                   np.zeros(48, dtype=int),
                                                                   (self.a * 6).value,
                                                                   (self.b * 12).value,
                                                                   (self.a * self.a).invminus().value])])
        Phi4 = Division_Polynomial(self.a, self.b, [1, Polynomial([np.concatenate((np.zeros(47, dtype=int), [4])),
                                                                   np.zeros(48, dtype=int),
                                                                    (self.a * 20).value,
                                                                    (self.b * 80).value,
                                                                    (self.a * self.a * 20).invminus().value,
                                                                    (self.a * self.b * 16).invminus().value,
                                                                    (self.a * self.a * self.a * 4 + self.b * self.b * 32).invminus().value])])

        Phi = [Phi0, Phi1, Phi2, Phi3, Phi4]

        for m in range(2, (l-1)//2+1):

            Phi2m1 = [(Phi[m+2] * Phi[m]) * (Phi[m] * Phi[m]), (Phi[m-1] * Phi[m+1]) * (Phi[m+1] * Phi[m+1])]
            Phi2m1 = self.replaceYSquared(Phi2m1)
            Phi2m1 = self.subtraction(Phi2m1[0], Phi2m1[1])
            Phi.append(Division_Polynomial(self.a, self.b, [Phi2m1[0], Phi2m1[1]]))

            Phi2m = [Phi[(m+1)+2] * Phi[(m+1)-1] * Phi[(m+1)-1], Phi[(m+1)-2] * Phi[(m+1)+1] * Phi[(m+1)+1]]
            Phi2m[0].h[0] -= 1
            Phi2m[1].h[0] -= 1
            Phi2m = self.replaceYSquared(Phi2m)
            Phi2m = self.subtraction(Phi2m[0], Phi2m[1])
            Phi2m = Division_Polynomial(self.a, self.b, [Phi2m[0], Phi2m[1]])
            Phi2m  = Phi2m * Phi[(m+1)] 
            Phi2m = Phi2m / 2
            Phi.append(Phi2m)

        return Phi

    def __str__(self):
        return (str(self.h))
    
    def __repr__(self):
        return (str(self.h))
    
    def subtraction(self, Part1, Part2):
        if Part1[0] != Part2[0]:
            print("Error: y not equal")
        result = [Part1[0], Part1[1] - Part2[1]]
        return result

    def __truediv__(self, other):
        if other == 2:
            return Division_Polynomial(self.a, self.b, [self.h[0], self.h[1] / 2])
            

    def replaceYSquared(self,Phi2m1):
        result = []
        for part in Phi2m1:
            part = part.h
            times_replace = part[0] // 2
            part[0] = part[0] % 2
            for _ in range(times_replace):
                short_Weierstrass = Polynomial([np.concatenate((np.zeros(47, dtype=int), [1])),
                                                np.zeros(48, dtype=int),
                                                self.a.value,
                                                self.b.value])
                part[1] *= short_Weierstrass
            
            result.append(part)
        return result

    def __mul__(self, other):
        y = self.h[0] + other.h[0]
        x = self.h[1] * other.h[1]
        return Division_Polynomial(self.a, self.b, [y,x])

def karatsuba_mul(a, b):
    n = max(len(a), len(b))
    if n == 1:
        if len(a) == 0 or len(b) == 0:
            return []
        return [a[0] * b[0]]
    n_2 = n // 2
    a1, a0 = a[:n_2], a[n_2:]
    b1, b0 = b[:n_2], b[n_2:]
    a1b1 = karatsuba_mul(a1, b1)
    a0b0 = karatsuba_mul(a0, b0)
    a1_plus_a0 = [ai + aj for ai, aj in zip_longest(a1, a0, fillvalue=fast_F47_hoch_48(np.zeros(48,dtype=int)))]
    b1_plus_b0 = [bi + bj for bi, bj in zip_longest(b1, b0, fillvalue=fast_F47_hoch_48(np.zeros(48,dtype=int)))]
    a1b1_plus_a0b0 = karatsuba_mul(a1_plus_a0, b1_plus_b0)
    piece = [ai + aj for ai, aj in zip_longest(a1b1, a0b0, fillvalue=fast_F47_hoch_48(np.zeros(48,dtype=int)))]
    middle_term = [ai - aj for ai, aj in zip_longest(a1b1_plus_a0b0, piece, fillvalue=fast_F47_hoch_48(np.zeros(48,dtype=int)))]
    result = [fast_F47_hoch_48(np.zeros(48,dtype=int)) for _ in range(len(a) + len(b) - 1)]
    for i, val in enumerate(a1b1):
        result[i] += val
    for i, val in enumerate(middle_term):
        result[i + n_2] += val
    for i, val in enumerate(reversed(a0b0)):
        result[-(i + 1)] += val
                                                                                                                                                                                                                                                                                                                                                                                                                    
    return result
