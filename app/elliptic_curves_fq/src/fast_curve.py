import numpy as np
import copy

class fast_F47_hoch_48:
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
        return np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13], dtype=int)
    
    def q(self):
        return 182262440382829085265332464749253545480222210363177678129189304510665330097954561
    
    def degree(self):
        return 48
    
    def __add__(self,other):
        ' Addition über dem Körper F(p^n)'
        result = (self.value + other.value) % self.p
        return fast_F47_hoch_48(result)
    
    def __sub__(self,other):
        ' Subtraktion über dem Körper F(p^n)'
        result = (self.value - other.value) % self.p
        return fast_F47_hoch_48(result)
    
    def invminus(self):
        ' gibt den Wert des Polynoms [0] - Vertreter zurück'
        result = (-self.value) % self.p
        return fast_F47_hoch_48(result)
    
    def __mul__(self, other):
        ' Multiplikation über dem Körper F(p^n) ohne Kürzung mod irreduziblem Poynom'
        if isinstance(other, int):
            return fast_F47_hoch_48((self.value * other) % self.p)
        ' Multiplikation über dem Körper F(p^n) ohne Kürzung mod irreduziblem Poynom'
        conv = np.convolve(self.value, other.value) % self.p
        'Kürzung des Polynoms mod irreduziblem Polynom'
        temp = conv[:24]
        temp2 = conv[24:48] - temp
        temp3 = (conv[48:72] - temp * 13)
        temp4  = conv[72:]
        temp5 = np.concatenate(([0],temp2[:23], [0]*24))
        temp5_shifted = np.roll(temp5, 24)
        result = (np.concatenate((temp2[23:],temp3,temp4)) - temp5 - temp5_shifted * 13) % self.p
        return(fast_F47_hoch_48(result))
    
    def mul2(self, value, other):
        value = value.value
        'Multiplikation über dem Körper F(p^n), spezifisch für Inverse'
        value = value[(len(other)-1):]
        conv = np.convolve(value, other) % self.p
        return fast_F47_hoch_48(conv)

    
    def __invert__(self):
        'gibt inverses Element eines Vertreters im Körper F(p^n) / ireduziblem Polynom an. Wird mit Hilfe des erweiterten Euklidischen Algorithmus für Polynome über Fp berechnet'
        a = copy.copy(self.ir_poly)
        b = copy.copy(self.value)
        c = []
        while sum(b) != 0:
            division = self.div(a,b)
            c += [division[0]]
            #division[1] = np.trim_zeros(division[1], 'f')
                
            a = b
            b = division[1]
        a = np.trim_zeros(a, 'f')
        if len(a) != 1:
            print(a)
            print("nicht irreduzibel")
            return
        inv_a = pow(a[0].item(),self.p-2,self.p)
        d = fast_F47_hoch_48(np.concatenate([np.zeros(47, dtype=int), [1]]))
        e = fast_F47_hoch_48(np.zeros(48, dtype=int))
        while c != []:
            temp = d
            d = e
            e = temp - self.mul2(e, c[-1])
            c.pop(-1)
        e.value = (e.value * inv_a ) % self.p 
        return fast_F47_hoch_48(e.value)

    def div(self,value, other):
        if np.sum(other) == 0:
            print("division by Zero")
            return None
        other = np.trim_zeros(other, 'f')
        value = np.trim_zeros(value, 'f')
        degree = len(other) - 1
        if len(value) < len(other):
            return [np.array([0]), value]
        floor = []
        while len(value) >= degree + 1:
            if value[0] == 0:
                value = value[1:]
                floor.append(0)   
            else:
                first_of_mod = value[0]
                facter = ((self.p - first_of_mod) * pow(other[0].item(),self.p-2,self.p)) % self.p
                value[:degree+1] = (value[:degree+1] + facter * other[:degree+1]) % self.p
                value = value[1:]
                floor.append(self.p-facter)
        return [np.array(floor),value]
        
    def __truediv__(self, other):
        ' Division über dem Körper F(p^n). Wird mit der Multiplikation des Inversen des Nenners berechnet'
        return(self * (~other) )

    def __eq__(self,other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        return np.array_equal(self.value, other.value)

    def __pow__(self,count):
        ' Wiederholte Multiplikation ( Potenz mit square and multiply. Laufzeit log(n))'
        one = np.zeros(48, dtype=int)
        one[-1] = 1
        result = fast_F47_hoch_48(one)
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

        self.a = fast_F47_hoch_48(np.array([38, 16, 45, 26, 10, 16, 42, 26, 37, 9, 18, 30, 8, 0, 42, 29, 9, 31, 0, 45, 18, 31, 45, 27, 6, 35, 40, 17, 24, 44, 32, 43, 2, 45, 7, 17, 37, 11, 42, 45, 15, 0, 11, 27, 43, 32, 8, 36]))
        self.b = fast_F47_hoch_48(np.array([30, 31, 29, 36, 34, 8, 7, 39, 40, 46, 6, 18, 2, 27, 10, 21, 30, 14, 21, 9, 13, 46, 32, 20, 23, 9, 19, 7, 36, 2, 39, 16, 39, 14, 19, 10, 40, 44, 33, 23, 44, 27, 4, 28, 18, 44, 32, 41]))
        self.Point=[self.x,self.y]

    def q(self):
        return 182262440382829085265332464749253545480222210363177678129189304510665330097954561

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
                s = (self.x * self.x * 3 + self.a) / (self.y * 2)
                x3 = s * s  - (self.x * 2)
                y3 = (s * (self.x - x3)) - self.y
                return fast_Curve_Point([x3,y3])    
            else:
                if self.x == x2:
                    return fast_Curve_Point("inf")
                else: 
                    s = (self.y-y2) / (self.x-x2)
                    x3 = s * s - self.x - x2
                    y3 = (s* ( self.x - x3)) -self.y
                    return fast_Curve_Point([x3,y3])
    def __sub__(self,other):
        'Subtraktion durch aufaddieren des inversen Punktes'
        return self + other.invminus()
    def invminus(self):
        if self.x == "inf":
            return self
        else: 
            return fast_Curve_Point([self.x, self.y.invminus()])
    def __mul__ (self, Faktor):
        ' Punkt Multiplikation sprich aufaddierung des selben Punktes n-mal. Mit square and multiply laufzeit von (log(n))'
        start = fast_Curve_Point("inf")
        counting = self
        while Faktor > 0:
            if Faktor % 2 == 1: start += counting
            counting += counting
            Faktor = Faktor // 2

        return start    


    def __eq__(self,other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        if type(other.x) == type(self.x):
            return (self.x == other.x and self.y == other.y)
        else:
            return False
    
    def on_Curve(self):
        ' Überprüft ob ein Punkt wirklich auf der Kurve ist, indem es checkt ob y^2 == x^3 + ax + b. Gint Bool zurück'
        if self.x == "inf" and self.y == "inf" : return True
        else:
            return (self.x * self.x * self.x + self.Curve.a * self.x + self.Curve.b)  == (self.y * self.y )

def start_point():
    ' Gibt den Startpunkt der Kurve zurück'
    x =  [29, 4, 24, 4, 45, 41, 34, 18, 5, 37, 21, 32, 38, 4, 45, 36, 8, 4, 0, 43, 44, 31, 5, 21, 38, 43, 28, 35, 40, 12, 19, 27, 24, 1, 30, 26, 15, 35, 45, 30, 14, 12, 21, 30, 45, 18, 13, 11]
    y =  [15, 2, 46, 42, 27, 17, 40, 22, 30, 18, 45, 24, 21, 25, 21, 11, 29, 36, 11, 25, 42, 15, 25, 17, 30, 35, 1, 2, 15, 7, 35, 20, 44, 27, 4, 11, 2, 46, 7, 17, 18, 7, 2, 5, 29, 11, 36, 39]
    return fast_Curve_Point([fast_F47_hoch_48(np.array(x)),fast_F47_hoch_48(np.array(y))])
