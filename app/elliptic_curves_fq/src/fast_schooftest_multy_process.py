'Schoof algorithmus, um Ordung der Elliptischen Kurve zu bestimmen'
import copy
import numpy as np
from itertools import zip_longest
import concurrent.futures
import time

inverse_list = np.array([0, 1, 24, 16, 12, 19, 8, 27, 6, 21, 33, 30, 4, 29, 37, 22, 3, 36, 34, 5, 40, 9, 15, 45, 2, 32, 38, 7, 42, 13, 11, 44, 25, 10, 18, 43, 17, 14, 26, 41, 20, 39, 28, 35, 31, 23, 46],dtype=int)

class fast_F47_hoch_46:
    '''
    Python implementation des Endlichen Körpers F(p^n) mit der Primzahl 47, und einem ireduziblem Polynom Grad 46
    '''
    def __init__(self,value):
        ' Konstruktor der Klasse mit irreduziblem Polynom über Fp als Liste, und Vertreter der Klasse, ebenfalls als Liste. Vetreter wird zuerst mit der Methode .formate gekürzt. Self.q = p^n und entspricht der Ordnung'
        self.p = 47
        self.value = value
        
    def __repr__(self):
        ' String von Fpn bei repr Command'
        return f"{self.value}"

    def __str__(self):
        return(f"{self.value}")
    
    def ir_poly(self):
        return np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], dtype=int)
    
    def q(self):
        return self.p**46
    
    def degree(self):
        return 46
    
    def __add__(self,other):
        ' Addition über dem Körper F(p^n)'
        result = (self.value + other.value) % self.p
        return fast_F47_hoch_46(result)
    
    def __sub__(self,other):
        ' Subtraktion über dem Körper F(p^n)'
        result = (self.value - other.value) % self.p
        return fast_F47_hoch_46(result)
    
    def invminus(self):
        ' gibt den Wert des Polynoms [0] - Vertreter zurück'
        result = (-self.value) % self.p
        return fast_F47_hoch_46(result)
    
    def __mul__(self, other):
        ' Multiplikation über dem Körper F(p^n) ohne Kürzung mod irreduziblem Poynom'
        if isinstance(other, int):
            return fast_F47_hoch_46((self.value * other) % self.p)
        ' Multiplikation über dem Körper F(p^n) ohne Kürzung mod irreduziblem Poynom'
        conv = np.convolve(self.value, other.value) % self.p
        'Kürzung des Polynoms mod irreduziblem Polynom'
        final = (conv[46:] - conv[:45] * 2) % 47
        final= np.append(conv[45],final)
        return(fast_F47_hoch_46(final))
    
    def mul2(self, value, other):
        'Multiplikation über dem Körper F(p^n), spezifisch für Inverse'
        value = value.value[(len(other)-1):]
        conv = np.convolve(value, other) % self.p
        return fast_F47_hoch_46(conv)

    
    def __invert__(self):
        'gibt inverses Element eines Vertreters im Körper F(p^n) / ireduziblem Polynom an. Wird mit Hilfe des erweiterten Euklidischen Algorithmus für Polynome über Fp berechnet'
        b = copy.copy(self.value)
        if sum(b) == b[-1]:
            b[-1] = inverse_list[b[-1]]
            return fast_F47_hoch_46(b)
        a = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2], dtype=int)
        
        c = []
        while sum(b) != 0:
            division = self.div(a,b)
            c += [division[0]]        
            a = b
            b = division[1]
        a = np.trim_zeros(a, 'f')
        if len(a) != 1:
            print(a)
            print("nicht irreduzibel")
            return
        inv_a = inverse_list[a[0]]
        d = fast_F47_hoch_46(np.concatenate([np.zeros(45, dtype=int), [1]]))
        e = fast_F47_hoch_46(np.zeros(46, dtype=int))
        while c != []:
            temp = d
            d = e
            e = temp - self.mul2(e, c[-1])
            c.pop(-1)
        e.value = (e.value * inv_a ) % self.p 
        return fast_F47_hoch_46(e.value)

    def div(self,value, other):
        if np.sum(other) == 0:
            print("division by Zero")
            return None
        other = np.trim_zeros(other, 'f')
        value = np.trim_zeros(value, 'f')
        degree = len(other) - 1
        if len(value) < len(other):
            return [np.array([0],dtype=int), value]
        floor = []
        while len(value) >= degree + 1:
            if value[0] == 0:
                value = value[1:]
                floor.append(0)   
            else:
                first_of_mod = value[0]
                other_inv = inverse_list[other[0]]
                facter = ((self.p - first_of_mod) * other_inv) % self.p
                value[:degree+1] = (value[:degree+1] + facter * other[:degree+1]) % self.p
                value = value[1:]
                floor.append(self.p-facter)
        return [np.array(floor,dtype=int),value]
        
    def __truediv__(self, other):
        ' Division über dem Körper F(p^n). Wird mit der Multiplikation des Inversen des Nenners berechnet'
        return(self * (~other) )

    def __eq__(self,other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        return np.array_equal(self.value, other.value)

    def __pow__(self,count):
        ' Wiederholte Multiplikation ( Potenz mit square and multiply. Laufzeit log(n))'
        one = np.zeros(46, dtype=int)
        one[-1] = 1
        result = fast_F47_hoch_46(one)
        counting = self
        while count > 0:
            if count % 2 == 1: result *= counting
            counting *= counting
            count = count // 2
        return result
        
class fast_Curve_Point:
    ' Klasse eines Punktes auf einer Bestimmten Elliptische Kurve'
    def __init__ (self, Point, a, b):
        'Konstruktor der Klasse. x und y werden vom Punkt eingetragen'
        if isinstance(Point, list):
            if isinstance(Point[0],str):
                self.x = "inf"
                self.y = "inf" 
            else:
                self.x = Point[0]
                self.y = Point[1]
        else:
            if Point == "inf":
                self.x = "inf"
                self.y = "inf"  

        self.a = a
        self.b = b

    def q(self):
        return 47 ** 46

    def __str__(self):
        ' Wenn Punkt geprinted wird (x,y) ausgedrückt'
        return f"({self.x}, {self.y})"
    def __repr__(self):
        ' Bei print falls in Liste, werden (x,y) ausgedrückt'
        return f"({self.x}, {self.y})"
    
    def __add__ (self, Point2):
        ' Addtion von zwei Punkten auf der Elliptischen Kurve'
        global total_div_time
        x2 = Point2.x
        y2 = Point2.y
        if isinstance(self.x,str):
            return fast_Curve_Point([x2,y2], self.a, self.b)
        elif isinstance(x2,str):
            return fast_Curve_Point([self.x,self.y], self.a, self.b)
        else:
            if x2 == self.x and y2 == self.y:
                if sum(self.y.value) == 0:
                    return fast_Curve_Point("inf", self.a, self.b)                
                d_x = (self.x * self.x * 3 + self.a)
                d_y = (self.y * 2)
                s = d_x / d_y
                x3 = s * s  - (self.x * 2)
                y3 = (s * (self.x - x3)) - self.y
                return fast_Curve_Point([x3,y3], self.a, self.b)    
            else:
                if self.x == x2:
                    return fast_Curve_Point("inf", self.a, self.b)
                else: 
                    d_y = (self.y-y2)
                    d_x = (self.x-x2)
                    s = d_y / d_x
                    x3 = s * s - self.x - x2
                    y3 = (s* ( self.x - x3)) -self.y
                    return fast_Curve_Point([x3,y3], self.a, self.b)
    def __sub__(self,other):
        'Subtraktion durch aufaddieren des inversen Punktes'
        return self + other.invminus()
    def invminus(self):
        if self.x == "inf":
            return self
        else: 
            return fast_Curve_Point([self.x, self.y.invminus()], self.a, self.b)
    def __mul__ (self, Faktor):
        ' Punkt Multiplikation sprich aufaddierung des selben Punktes n-mal. Mit square and multiply laufzeit von (log(n))'
        start = fast_Curve_Point("inf", self.a, self.b)
        counting = self
        if Faktor < 0:
            Faktor = -Faktor
            counting = counting.invminus()
        while Faktor > 0:
            if Faktor % 2 == 1: start += counting
            counting += counting
            Faktor = Faktor // 2

        return start    

    def __eq__(self,other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        if isinstance(other, str):
            return isinstance(self.x, str)
        if type(other.x) == type(self.x):
            return (self.x == other.x and self.y == other.y)
        else:
            return False
    
    def on_Curve(self):
        ' Überprüft ob ein Punkt wirklich auf der Kurve ist, indem es checkt ob y^2 == x^3 + ax + b. Gint Bool zurück'
        if isinstance(self.x, str):
            return isinstance(self.y, str)
        else:
            return (self.x * self.x * self.x + self.a * self.x + self.b)  == (self.y * self.y )

def start_point(a ,b, x, y):
    ' Gibt den Startpunkt der Kurve zurück'
    return fast_Curve_Point([x,y], a, b)

# Python-Programm für den chinesischen Restsatz Algorithmus
def extended_gcd(a, b):
    'erweiterter Euklidischer Algoritmus'
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return [gcd, y - (b // a) * x, x]
 
def solve_for_a(Modules, Rests):
    'Chinesischer Restsatz. Liste von verschiedenen Modulos und eine andere List mit zugrhörigen Resten. Die Zahl für welche dies alles zutrifft, wird hier berechnet'
    adds = []
    n = 1
    for i in Modules: 
        n *= i
    for count, i in enumerate (Modules):
        same = n // i
        inverses=extended_gcd(same,i)
        if inverses[1] > 0: 
            real = inverses[1]
        else: 
            real = inverses[1]%i
        adds += [(real * Rests[count] * same) % n]
    final = sum(adds) % n
    return final

class NotIrreducibleError(ValueError):
    def __init__(self, message, obj):
        super().__init__(message)
        self.facter = obj

class TortionGroup:
    def __init__(self, a, b, Phi_l, Point):
        self.a = a
        self.b = b
        self.Phi_l = Phi_l
        self.f = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1])),
                                np.zeros(46,dtype=int),
                                a.value,
                                b.value]) # x^3 + ax + b
        if isinstance(Point, list):
            if isinstance(Point[0],str):
                self.x = "inf"
                self.y = "inf" 
            else:
                self.x = Point[0]
                self.y = Point[1]
        else:
            if Point == "inf":
                self.x = "inf"
                self.y = "inf" 

        self.Point=[self.x,self.y]
    
    def __str__(self):
        return (str(self.Point))

    def __add__(self, Point2):
        x2 = Point2.x
        y2 = Point2.y
        if isinstance(self.x,str):
            return TortionGroup(self.a,self.b,self.Phi_l,[x2,y2])
        elif isinstance(x2,str):
            return TortionGroup(self.a,self.b,self.Phi_l,[self.x,self.y])
        else:
            if x2 == self.x and y2 == self.y:
                if (self.y).sum() == 0:
                    return TortionGroup(self.a, self.b, self.Phi_l, "inf")                
                d_x = (((self.x * self.x) % self.Phi_l) * 3 + self.a)
                d_y = (((self.y * self.f) % self.Phi_l) * 2)
                r = d_x.__truediv__(d_y, self.Phi_l)
                x3 =((((self.f * r) % self.Phi_l) * r) % self.Phi_l) - (self.x * 2)
                y3 = ((r * (self.x - x3)) % self.Phi_l) - self.y
                return TortionGroup(self.a, self.b, self.Phi_l, [x3,y3])    
            else:
                if self.x == x2:
                    return TortionGroup(self.a, self.b, self.Phi_l, "inf")
                else: 
                    d_y = self.y - y2
                    d_x = self.x - x2
                    r = d_y.__truediv__(d_x, self.Phi_l)
                    x3 = ((((self.f * r) % self.Phi_l) * r) % self.Phi_l) - self.x - x2
                    y3 = ((r * ( self.x - x3))  % self.Phi_l )  - self.y
                    return TortionGroup(self.a, self.b, self.Phi_l, [x3,y3])
                
    def __eq__(self, Point2):
        if isinstance(self.x,str):
            if isinstance(Point2.x,str):
                return True
            else:
                return False
        elif isinstance(Point2.x,str):
            return False
        else:
            return self.x == Point2.x and self.y == Point2.y
    def invminus(self):
        if isinstance(self.x,str):
            return TortionGroup(self.a,self.b,self.Phi_l,[self.x,self.y])
        else:
            return TortionGroup(self.a,self.b,self.Phi_l,[self.x,copy.copy(self.y).invminus()])

class Polynomial:
    ' Klasse eines Polynom mit Koeffizienten in F(p^n)'
    def __init__(self,value):
        if len(value) == 0:
            self.value = []
        elif isinstance(value[0],np.ndarray):
            self.value = [fast_F47_hoch_46(value[i]) for i in range(len(value))]
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

    def __add__(self, other):
        if isinstance(other,fast_F47_hoch_46):
            self.value[-1] += other
            return self
        else:
            pass

    def __mul__(self, other):
        if isinstance(other,int):
            result = [i * other for i in self.value]
            return Polynomial(result)
        result = karatsuba_mul(self.value, other.value)
        return Polynomial(result)
        return self.__mul2__(other)
    
    def __mul2__(self, other):
        n = len(self.value)
        m = len(other.value)
        result = [fast_F47_hoch_46(np.zeros(46,dtype=int)) for _ in range(n + m - 1)]
        for i in range(n):
            for j in range(m):
                result[i+j] += self.value[i] * other.value[j]
        return Polynomial(result)
    
    def __truediv__(self,other, Modulos):
        if isinstance(other,int):
            if other == 2:
                self.value = [i * 24 for i in self.value]
                return (self)
        else:
            return (self * other.__invert__(Modulos)) % Modulos

    def sum(self):
        Summe =0
        for i in self.value:
            Summe +=sum(i.value)
        return (Summe)
    
    def __sub__(self,other):
        if len(self.value) < len(other.value):
            self.value = [fast_F47_hoch_46(np.zeros(46,dtype=int)) for _ in range(len(other.value) - len(self.value))] + self.value
        elif len(self.value) > len(other.value):
            other.value = [fast_F47_hoch_46(np.zeros(46,dtype=int)) for _ in range(len(self.value) - len(other.value))] + other.value
        result = [self.value[i] - other.value[i] for i in range(len(self.value))]
        index = 0
        while len(result) > (index + 1) and np.sum(result[index].value) == 0:
            index += 1
        return Polynomial(result[index:])
    
    def __mod__(self,other):
        return (self.div(other))[1]
    
    def __pow__(self,other,Modulos, l = 2, place = 'remainder mod2'):
        start_time = time.perf_counter()
        hours = 1
        Dynamisch = copy.copy(self)
        Value = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1]))]) #Startwert 1
        while other > 0:
            if other % 2 == 1:
                Value = (Value * Dynamisch)
                Value = Value % Modulos
            Dynamisch = (Dynamisch * Dynamisch) 
            Dynamisch = Dynamisch % Modulos
            temp_time = time.perf_counter()

            if (temp_time - start_time) > 3600 * hours:
                hours = ((temp_time - start_time) // 3600) + 1
                try:
                    print(f'\033[37mwith l = {l} in {place} with {(temp_time - start_time)/3600} hours at power {other/1} which is {82509026882222311120566982684134696912730742581791615268985651657159497554529/other} times smaller than q')
                except Exception as e:
                    print(f"Caught an error: {e}")
            other = other // 2
        return Value
    
    def div(self, other):
        'Argumente g(x) und h(x), gibt eindeutig bestimmtes q(x) und r(x) sodass g(x) = q(x) * h(x) + r(x)'
        value = copy.copy(self.value)
        if len(value) < len(other.value):
            return [Polynomial([]),self]
        #kürzen um len(self.value)- len(other.value) + 1 Stellen
        floor = []
        k = len(value)- len(other.value) + 1
        other_inverse = ~other.value[0]
        for i in range(k):
            facter = value[i] * other_inverse
            floor.append(facter)
            facter = facter.invminus()
            for j in range(len(other.value)):
                value[i + j] = (value[i + j]  + (facter * other.value[j]))
        index = k
        if len(value) == index:
            return [Polynomial(floor),Polynomial([])]
        while np.sum(value[index].value) == 0:
            index += 1
            if len(value) == index:
                return [Polynomial(floor), Polynomial([])]
        return [Polynomial(floor), Polynomial(value[index:])]
    
    def __invert__(self, Modulos):
        'Berechnet das Inverse eines Polynoms'
        a = copy.copy(Modulos)
        b = copy.copy(self)
        c = []
        while len(b.value) > 0:
            division = a.div(b)
            c.append(division[0])
            a = b
            b = division[1]
        if len(a.value) != 1:
            print(f"\033[32mKein Inverses")
            raise NotIrreducibleError("Kein Inverses",a)
        else:
            inv_a = ~a.value[0]
            d = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1]))])
            e = Polynomial([np.concatenate((np.zeros(45,dtype=int), [0]))])
            while len(c) > 0:
                f = d - e * c.pop()
                d = e
                e = f
            e.value  = [i * inv_a for i in e.value]
            return e
    
    def __eq__(self,other):
        if len(self.value) != len(other.value):
            return False
        for i in range(len(self.value)):
            if self.value[i] != other.value[i]:
                return False
        return True
    
    def invminus(self):
        result = [(self.value[i].invminus()) for i in range(len(self.value))]
        return Polynomial(result)

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
    a1_plus_a0 = [ai + aj for ai, aj in zip_longest(a1, a0, fillvalue=fast_F47_hoch_46(np.zeros(46,dtype=int)))]
    b1_plus_b0 = [bi + bj for bi, bj in zip_longest(b1, b0, fillvalue=fast_F47_hoch_46(np.zeros(46,dtype=int)))]
    a1b1_plus_a0b0 = karatsuba_mul(a1_plus_a0, b1_plus_b0)
    piece = [ai + aj for ai, aj in zip_longest(a1b1, a0b0, fillvalue=fast_F47_hoch_46(np.zeros(46,dtype=int)))]
    middle_term = [ai - aj for ai, aj in zip_longest(a1b1_plus_a0b0, piece, fillvalue=fast_F47_hoch_46(np.zeros(46,dtype=int)))]
    result = [fast_F47_hoch_46(np.zeros(46,dtype=int)) for _ in range(len(a) + len(b) - 1)]
    for i, val in enumerate(a1b1):
        result[i] += val
    for i, val in enumerate(middle_term):
        result[i + n_2] += val
    for i, val in enumerate(reversed(a0b0)):
        result[-(i + 1)] += val
                                                                                                                                                                                                                                                                                                                                                                                                                    
    return result

class Division_Polynomial():
    
    def __init__(self, a, b, h=[0,0]):
        self.a = a
        self.b = b
        self.h = h

    def get_division_polynomial(self, l):
        Phi0 = Division_Polynomial(self.a, self.b ,[0, Polynomial([np.zeros(46, dtype=int)])])
        Phi1 = Division_Polynomial(self.a, self.b, [0, Polynomial([np.concatenate((np.zeros(45, dtype=int), [1]))])])
        Phi2 = Division_Polynomial(self.a, self.b, [1, Polynomial([np.concatenate((np.zeros(45, dtype=int), [2]))])])
        Phi3 = Division_Polynomial(self.a, self.b, [0, Polynomial([np.concatenate((np.zeros(45, dtype=int), [3])),
                                                                   np.zeros(46, dtype=int),
                                                                   (self.a * 6).value,
                                                                   (self.b * 12).value,
                                                                   (self.a * self.a).invminus().value])])
        Phi4 = Division_Polynomial(self.a, self.b, [1, Polynomial([np.concatenate((np.zeros(45, dtype=int), [4])),
                                                                   np.zeros(46, dtype=int),
                                                                    (self.a * 20).value,
                                                                    (self.b * 80).value,
                                                                    (self.a * self.a * 20).invminus().value,
                                                                    (self.a * self.b * 16).invminus().value,
                                                                    (self.a * self.a * self.a * 4 + self.b * self.b * 32).invminus().value])])

        Phi = [Phi0, Phi1, Phi2, Phi3, Phi4]
        try:
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
                if m%5 == 0:
                    print(len(Phi))
        except KeyboardInterrupt:
            print("Keyboard interrupt bei:", m)

        return Phi
    
    def get_primes(self, l, Phi):
        List_primes = [59, 61, 67, 71, 73, 79, 83, 89]
        Phi = Phi + [None] * (89-l)
        for prime in List_primes:
            m = prime // 2
            Phi2m1 = [(Phi[m+2] * Phi[m]) * (Phi[m] * Phi[m]), (Phi[m-1] * Phi[m+1]) * (Phi[m+1] * Phi[m+1])]
            Phi2m1 = self.replaceYSquared(Phi2m1)
            Phi2m1 = self.subtraction(Phi2m1[0], Phi2m1[1])
            Phi[prime] = Division_Polynomial(self.a, self.b, [Phi2m1[0], Phi2m1[1]])
            print(prime)
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
            return Division_Polynomial(self.a, self.b, [self.h[0], self.h[1].__truediv__(2, None)])
            

    def replaceYSquared(self,Phi2m1):
        result = []
        for part in Phi2m1:
            part = part.h
            times_replace = part[0] // 2
            part[0] = part[0] % 2
            for _ in range(times_replace):
                short_Weierstrass = Polynomial([np.concatenate((np.zeros(45, dtype=int), [1])),
                                                np.zeros(46, dtype=int),
                                                self.a.value,
                                                self.b.value])
                part[1] = part[1] * short_Weierstrass
            
            result.append(part)
        return result

    def __mul__(self, other):
        y = self.h[0] + other.h[0]
        x = self.h[1] * other.h[1]
        return Division_Polynomial(self.a, self.b, [y,x])
    
    def __sub__(self, other):
        pass

def remainderT2(a, b): 
    'calculate ggt((x^q-x),x^3+ax+b)'
    q = a.q()
    Curve = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1])),
                        np.zeros(46,dtype=int),
                        a.value,
                        b.value]) # x^3 + ax + b
    Value = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1]))
                        ,np.zeros(46,dtype=int)])
    Value = Value.__pow__(q,Curve)

    Value.value[-2] -= fast_F47_hoch_46(np.concatenate((np.zeros(45,dtype=int), [1])))
    if Value.sum() == 0:
        return 0
    else:
        fx = Curve
        b = Value
        temp = fx % b
        while temp.sum() != 0:
            temp, b = b % temp, temp

        return int(len(b.value) == 1)

def calculate_x_part(Pi_l_x, q, Phi_l,l):
    # Your calculation for x part
    Pi_l_x = Pi_l_x.__pow__(q, Phi_l,l,f'calculate Pi_l_x')
    print(f'\033[32mcalculated Pi_{l}_x')
    Pi_l_squared_x = Pi_l_x.__pow__(q, Phi_l,l,f'calculate Pi_l_squared_x')
    print(f'\033[32mcalculated Pi_{l}_squared_x')
    return Pi_l_x, Pi_l_squared_x

def calculate_y_part(Pi_l_y, q, Phi_l,l):
    # Your calculation for y part
    Pi_l_y = Pi_l_y.__pow__(q//2, Phi_l,l,f'calculate Pi_l_y')
    print(f'\033[32mcalculated Pi_{l}_y')
    Pi_l_squared_y = Pi_l_y.__pow__(q+1, Phi_l,l,f'calculate Pi_l_squared_y')
    print(f'\033[32mcalculated Pi_{l}_squared_y')
    return Pi_l_y, Pi_l_squared_y

def remainderTl(a, b, l, Phi_l):
    'calculate remainder t mod l'
    q = a.q()
    ql = q % l
    if ql > l // 2:
        ql = ql - l
    
    Pi_l_x = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1])),
                                        np.zeros(46,dtype=int)]) #Startwert x
    Pi_l_y = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1])),
                                        np.zeros(46,dtype=int),
                                        a.value,
                                        b.value]) #x^3 + ax + b
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        # Submit tasks for x and y parts
        future_x = executor.submit(calculate_x_part, Pi_l_x, q, copy.copy(Phi_l),l)
        future_y = executor.submit(calculate_y_part, Pi_l_y, q, copy.copy(Phi_l),l)
        
        # Retrieve results in the order they were submitted
        Pi_l_x, Pi_l_squared_x = future_x.result()
        Pi_l_y, Pi_l_squared_y = future_y.result()
        
    '''
    Pi_l_x = Pi_l_x.__pow__(q, Phi_l)
    Pi_l_y = Pi_l_y.__pow__(q//2, Phi_l)
    print(f'calculated Pi_{l}')
    Pi_l_squared_x = Pi_l_x.__pow__(q, Phi_l)
    Pi_l_squared_y = Pi_l_y.__pow__(q+1, Phi_l)
    print(f'calculated Pi_{l}_squared')'''

    Pi_l = TortionGroup(a,b,Phi_l,[Pi_l_x,Pi_l_y])
    Pi_l_squared = TortionGroup(a,b,Phi_l,[Pi_l_squared_x,Pi_l_squared_y])

    ql1_x = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1])),
                            np.zeros(46,dtype=int)]) #Startwert x
    print(f'\033[32m {ql} ql')
    if ql > 0:
        ql1_y = Polynomial([np.concatenate((np.zeros(45,dtype=int), [1]))]) #Startwert 1
    else:
        ql1_y = Polynomial([np.concatenate((np.zeros(45,dtype=int), [46]))])
        ql = -ql
    Dynamisch = TortionGroup(a,b,Phi_l,[ql1_x,ql1_y])
    ql1 = TortionGroup(a,b,Phi_l,'inf')
    try:
        while True:
            print(f'\033[37m {ql} ql')
            if ql % 2 == 1: 
                ql1 += Dynamisch
            ql = ql // 2
            if ql == 0:
                break
            Dynamisch += Dynamisch
        test = Pi_l_squared + ql1

        Phi_i = TortionGroup(a,b,Phi_l,'inf')
        
        for i in range(0, l//2 + 1):
            print(f'\033[37miteration c = {i} for l = {l}')
            if test == Phi_i:
                print(f'\033[31mfound t = {i} for l = {l}')
                return i
            elif test == Phi_i.invminus():
                print(f'\033[31mfound t = {-i + l} for l = {l}')
                return -i + l
            Phi_i = Phi_i + Pi_l
    except NotIrreducibleError as e:
        facter = e.facter
        return remainderTl(a, b, l, facter)
    print('\033[31mhaven\'t found t')

def main_schoof(a, b, x, y,pools = 8):
    global total_total_start
    x = fast_F47_hoch_46(x)
    y = fast_F47_hoch_46(y)    
    a = fast_F47_hoch_46(a)
    b = fast_F47_hoch_46(b)
    start_div_poly = Division_Polynomial(a, b)
    div_poly = start_div_poly.get_division_polynomial(55)
    div_poly = start_div_poly.get_primes(55, div_poly)
    Phi = []
    for i in div_poly:
        if i == None:
            Phi.append(None)
        else:
            Phi.append(i.h[1])
    print('generated Division Polynomials')
    total_total_start = time.perf_counter()
    q = a.q()

    List_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 53, 59, 61, 67, 71, 73, 79, 83, 89]
    List_primes.reverse()
    primecount = 505717912688203207886181651092730

    t2 = remainderT2(a, b)
    print(f'\033[31mfound t = {t2} for 2')

    with concurrent.futures.ProcessPoolExecutor(max_workers=pools//2) as executor:
        Tlwithout2 = list(executor.map(remainderTl, [a] * len(List_primes), [b] * len(List_primes), List_primes, [Phi[prime] for prime in List_primes]))
    
    Tl = [t2] + list(reversed(Tlwithout2))
    List_primes.reverse()
    StartPoint = start_point(a,b,x,y)
    t = solve_for_a([2] + List_primes,Tl)
    bound = 2 * 47**23
    checkrange = bound // primecount + 1
    under = t + checkrange * primecount
    UnderPoint = StartPoint * (q + 1 - under)
    StepPoint = StartPoint * primecount
    for i in range(1, (2 * checkrange)+ 2):
        UnderPoint += StepPoint
        if UnderPoint == 'inf':
            t = under - i * primecount
            order = q + 1 - t
            print(f'\033[31mfound order')
            break

    return [[q,t], order, Tl]
        
if __name__ == '__main__':
    x = np.array([7, 4, 7, 17, 9, 5, 23, 32, 13, 0, 22, 25, 43, 34, 43, 11, 44, 38, 8, 36, 37, 9, 24, 31, 20, 37, 33, 45, 45, 22, 8, 20, 45, 3, 30, 21, 46, 19, 8, 14, 31, 3, 33, 9, 46, 15],dtype=int)
    y = np.array([41, 13, 25, 8, 19, 1, 13, 45, 42, 34, 43, 23, 7, 35, 23, 37, 15, 5, 22, 4, 42, 43, 17, 28, 10, 28, 41, 17, 36, 39, 10, 40, 25, 6, 39, 40, 24, 35, 28, 38, 16, 45, 37, 30, 19, 14],dtype=int)   
    a = np.array([3, 17, 22, 25, 41, 7, 10, 15, 15, 10, 37, 36, 29, 38, 37, 12, 26, 2, 20, 7, 22, 6, 39, 7, 16, 10, 46, 23, 19, 0, 18, 36, 7, 27, 4, 29, 34, 45, 27, 25, 12, 38, 37, 38, 38, 45],dtype=int)
    b = np.array([10, 29, 40, 5, 22, 46, 26, 38, 40, 41, 26, 46, 32, 41, 29, 28, 29, 0, 27, 13, 20, 38, 36, 33, 38, 10, 20, 4, 41, 34, 24, 7, 40, 6, 17, 24, 31, 10, 39, 46, 26, 38, 27, 27, 17, 45],dtype=int)
    import time
    total_total_start = time.perf_counter()
    try:
        print(f'\033[34m{main_schoof(a, b, x, y,10)}')
    except KeyboardInterrupt:
        pass    
    print(f'\033[34m{time.perf_counter() - total_total_start} total_total_time')
    print(f'\033[0m')