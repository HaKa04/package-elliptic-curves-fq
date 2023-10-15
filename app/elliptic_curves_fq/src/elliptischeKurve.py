'''Implementation von elliptischen Kurven und deren Aretmetic über endliche Körper'''
from .endlicheKoerper_Fp import Fp
from .endlicherKoerper_Fpn import Fpn
import math

class curve:
    ' Klasse einer Eliptischen Kurve über Fp'
    def __init__(self, a, b, p, Point, order):
        'Konstruktor der Klasse. Parameter a, b, p, Startpunkt, Ordnung'
        self.a = Fp(a,p)
        self.b = Fp(b,p)
        self.p = p
        self.ord = order
        self.startpoint = Points([Fp(Point[0],p),Fp(Point[1],p)],self)
    def __str__(self):
        return f'curve( a = {self.a}, b = {self.b}, p = {self.p}, Startpoint = {self.startpoint}, ord = {self.ord})'
    
    def bound(self):
        ' Ordnung der Gruppe der elliptischen Kurve nach Hasses Abschätzung gege unten und oben'
        return [int(self.p+1-2*math.sqrt(self.p)), math.ceil(self.p+1+2*math.sqrt(self.p))]
    
    def compute(self,x,y):
        ' Gibt den Wert von links und rechts der Gleichung: y^2 = x^3 + ax + b an, mit Argumenten x und y'
        if isinstance(x,Fp):
            return [ (x**3 + x * self.a + self.b).value, (y**2).value]
        else:
            return[(x**3 + x * self.a.value + self.b.value) % self.p, (y**2 %self.p)]

    def discriminante_is_zero(self):
        ' Diskrmminante = 4a^3 + 27b^2. Falls dies 0 ist True zurückgegeben. Ansonsten False'
        disc = (self.a * self.a * self.a * 4 + self.b * self.b * 27)
        if disc.value == 0:
            return True
        else: return False
                
class curve_Fpn(curve):
    'Klasse einer Eliptischen Kurve über Fpn'
    def __init__(self,a,b,p,ir_poly,Point,order):
        'Konstruktor der Klasse. Parameter a, b, p, ir_poly, Startpunkt, Ordnung'
        self.a = Fpn(p,ir_poly,a)
        self.b = Fpn(p,ir_poly,b)
        self.p = p
        self.ord = order
        self.ir_poly = ir_poly
        self.q = p ** (len(ir_poly)-1)
        self.startpoint = Points([Fpn(p,ir_poly,Point[0]),Fpn(p,ir_poly,Point[1])],self)
    def __str__(self):
        return f'curve_Fpn( a = {self.a}, b = {self.b}, p = {self.p}, ir_poly = {self.ir_poly}, Startpoint = {self.startpoint}, ord = {self.ord})'
    
    def bound(self):
        ' Ordnung der Gruppe der elliptischen Kurve nach Hasses Abschätzung gege unten und oben'
        return [int(self.q+1-2*math.sqrt(self.q)), math.ceil(self.q+1+2*math.sqrt(self.q))]
    def compute(self,x,y):
        ' Gibt den Wert von links und rechts der Gleichung: y^2 = x^3 + ax + b an, mit Argumenten x und y'
        if not isinstance(x,Fpn):
            x = Fpn(self.p, self.ir_poly,x)
            y = Fpn(self.p, self.ir_poly,y)
        return [(x**3 + x * self.a + self.b).value, (y**2).value]
        
    def discriminante_is_zero(self):
        ' Diskrmminante = 4a^3 + 27b^2. Falls dies 0 ist True zurückgegeben. Ansonsten False.'
        disc = (self.a * self.a * self.a * 4 + self.b * self.b * 27)
        if sum(disc.value) == 0:
            return True
        else: return False  
class Points:
    ' Klasse eines Punktes auf einer Bestimmten elliptische Kurve'
    def __init__ (self, Point, Curve):
        'Konstruktor der Klasse. x und y werden vom Punkt eingetragen'
        if Point == "inf" or Point == ["inf", "inf"]:
            self.x = "inf"
            self.y = "inf"
        elif isinstance(Point[0],Fp):
            self.x = Point[0]
            self.y = Point[1]
        elif isinstance(Point[0],Fpn):
            self.x = Point[0]
            self.y = Point[1]
        elif isinstance(Point[0],int):
            self.x = Fp(Point[0], Curve.p)
            self.y = Fp(Point[1], Curve.p)
        elif isinstance(Point[0],list):
            self.x = Fpn(Curve.p, Curve.ir_poly, Point[0])
            self.y = Fpn(Curve.p, Curve.ir_poly, Point[1])
        self.Curve = Curve
        self.Point=[self.x,self.y]

    def __str__(self):
        ' Wenn Punkt geprinted wird (x,y) ausgedrückt'
        return f"({self.x}, {self.y})"
    def __repr__(self):
        ' Bei print falls in Liste, werden (x,y) ausgedrückt'
        return f"({self.x}, {self.y})"
        
    def __add__ (self, Point2):
        ' Addtion von zwei Punkten auf der elliptischen Kurve'
        x2 = Point2.x
        y2 = Point2.y
        if self.x == "inf" and self.y == "inf":
            return Points([x2,y2],self.Curve)
        elif x2 == "inf" and y2 == "inf":
            return Points([self.x,self.y],self.Curve)
        else:
            if x2 == self.x and y2 == self.y:
                if isinstance(self.y,Fpn):
                    if sum(self.y.value) == 0:
                        return Points("inf",self.Curve)
                
                elif self.y == 0: return Points("inf",self.Curve)
                
                s = (self.x * self.x * 3 + self.Curve.a) / (self.y * 2)
                x3 = s * s  - (self.x * 2)
                y3 = (s * (self.x - x3)) - self.y
                return Points([x3,y3],self.Curve)    
            else:
                if self.x == x2:
                    return Points("inf",self.Curve)
                else: 
                    s = (self.y-y2)/(self.x-x2)
                    x3 = s * s - self.x - x2
                    y3 = (s* ( self.x - x3)) -self.y
                    return Points([x3,y3], self.Curve)
    def __sub__(self,other):
        'Subtraktion durch aufaddieren des inversen Punktes'
        return self + other.invminus()
    def invminus(self):
        'Gibt den inversen Punkt -P wider'
        if self.x == "inf":
            return self
        else: 
            return Points([self.x, self.y.invminus()], self.Curve)
            return
    def __mul__ (self, Faktor):
        ' Punkt Multiplikation sprich aufaddierung des selben Punktes n-mal. Mit square and multiply laufzeit von (log(n))'
        start = Points("inf",self.Curve)
        counting = self
        while Faktor > 0:
            if Faktor % 2 == 1: start += counting
            counting += counting
            Faktor = Faktor // 2

        return start    
    def __eq__(self,other):
        'Gibt Boolien zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        return (self.x == other.x and self.y == other.y and self.Curve == other.Curve)
    
    def generate(self):
        'Gruppe, die mit wiederholter addition von einem Punkt erzeugt wird. Laufzeit log(q) und smoit nur bei kleinen Kurven Möglich'
        if self.x == "inf": return [self]
        Listen = [self]
        i=-1
        while True:
            i+=1
            Listen.append(self + Listen[-1])
            if Listen[-1].x == "inf" :
                break
        return Listen
    def on_Curve(self):
        ' Überprüft ob ein Punkt wirklich auf der Kurve ist, indem es checkt ob y^2 == x^3 + ax + b. Gint Bool zurück'
        if self.x == "inf" and self.y == "inf" : return True
        else:
            return (self.x * self.x * self.x + self.Curve.a * self.x + self.Curve.b)  == (self.y * self.y )