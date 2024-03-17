import numpy as np
import copy

inverse_list = np.array([0, 1, 24, 16, 12, 19, 8, 27, 6, 21, 33, 30, 4, 29, 37, 22, 3, 36, 34, 5, 40, 9, 15, 45, 2, 32, 38, 7, 42, 13, 11, 44, 25, 10, 18, 43, 17, 14, 26, 41, 20, 39, 28, 35, 31, 23, 46],dtype=int)

class fast_F47_hoch_46:
    '''
    Python implementation des Endlichen Körpers F(p^n) mit der Primzahl p, und einem ireduziblem Polynom Grad n
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
    def __init__ (self, Point):
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

        self.a = fast_F47_hoch_46(np.array([3, 17, 22, 25, 41, 7, 10, 15, 15, 10, 37, 36, 29, 38, 37, 12, 26, 2, 20, 7, 22, 6, 39, 7, 16, 10, 46, 23, 19, 0, 18, 36, 7, 27, 4, 29, 34, 45, 27, 25, 12, 38, 37, 38, 38, 45],dtype=int))
        self.b = fast_F47_hoch_46(np.array([10, 29, 40, 5, 22, 46, 26, 38, 40, 41, 26, 46, 32, 41, 29, 28, 29, 0, 27, 13, 20, 38, 36, 33, 38, 10, 20, 4, 41, 34, 24, 7, 40, 6, 17, 24, 31, 10, 39, 46, 26, 38, 27, 27, 17, 45],dtype=int))
        self.Point=[self.x,self.y]

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
        x2 = Point2.x
        y2 = Point2.y
        if isinstance(self.x,str):
            return fast_Curve_Point([x2,y2])
        elif isinstance(x2,str):
            return fast_Curve_Point([self.x,self.y])
        else:
            if x2 == self.x and y2 == self.y:
                if sum(self.y.value) == 0:
                    return fast_Curve_Point("inf")                
                d_x = (self.x * self.x * 3 + self.a)
                d_y = (self.y * 2)
                s = d_x / d_y
                x3 = s * s  - (self.x * 2)
                y3 = (s * (self.x - x3)) - self.y
                return fast_Curve_Point([x3,y3])    
            else:
                if self.x == x2:
                    return fast_Curve_Point("inf")
                else: 
                    d_y = (self.y-y2)
                    d_x = (self.x-x2)
                    s = d_y / d_x
                    x3 = s * s - self.x - x2
                    y3 = (s* ( self.x - x3)) -self.y
                    return fast_Curve_Point([x3,y3])
    def __sub__(self,other):
        'Subtraktion durch aufaddieren des inversen Punktes'
        return self + other.invminus()
    def invminus(self):
        if isinstance(self.x,str):
            return self
        else: 
            return fast_Curve_Point([self.x, self.y.invminus()])
    def __mul__ (self, Faktor):
        ' Punkt Multiplikation sprich aufaddierung des selben Punktes n-mal. Mit square and multiply laufzeit von (log(n))'
        start = fast_Curve_Point("inf")
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

def start_point():
    ' Gibt den Startpunkt der Kurve zurück'
    x = [7, 4, 7, 17, 9, 5, 23, 32, 13, 0, 22, 25, 43, 34, 43, 11, 44, 38, 8, 36, 37, 9, 24, 31, 20, 37, 33, 45, 45, 22, 8, 20, 45, 3, 30, 21, 46, 19, 8, 14, 31, 3, 33, 9, 46, 15]
    y = [41, 13, 25, 8, 19, 1, 13, 45, 42, 34, 43, 23, 7, 35, 23, 37, 15, 5, 22, 4, 42, 43, 17, 28, 10, 28, 41, 17, 36, 39, 10, 40, 25, 6, 39, 40, 24, 35, 28, 38, 16, 45, 37, 30, 19, 14]
    return fast_Curve_Point([fast_F47_hoch_46(np.array(x,dtype=int)),fast_F47_hoch_46(np.array(y,dtype=int))])  
