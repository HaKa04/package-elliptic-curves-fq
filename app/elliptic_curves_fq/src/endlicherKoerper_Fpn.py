'implementation der Klasse F(p^n)'
import copy
from .endlicheKoerper_Fp import Fp
class Fpn:
    '''
    Python implementation des Endlichen Körpers F(p^n) mit der Primzahl p, und einem ireduziblem Polynom Grad n
    '''
    def __init__(self,p,ir_poly,value):
        ' Konstruktor der Klasse mit irreduziblem Polynom über Fp als Liste, und Vertreter der Klasse, ebenfalls als Liste. Vetreter wird zuerst mit der Methode .formate gekürzt. Self.q = p^n und entspricht der Ordnung'
        self.p = p
        self.ir_poly = ir_poly
        self.degree = len(ir_poly)-1
        self.value = self.formate(value,self.ir_poly)
        self.q = self.p ** self.degree
        
    def print_value(self):
        ' Mit Printvalue, wird Vetreter als Liste ausgedrückt'
        print(self.value)

    def __repr__(self):
        ' In einer Liste wird Fpn(Vertreter) ausgedrückt'
        return f"Fpn({self.value})"

    def __str__(self):
        return(f"Fpn({self.value})")
    
    def make_Fpn(self,other):
        'Macht other zur Klasse Fpn'
        if (not isinstance(other, Fpn)):
            if isinstance(other,int):
                other = Fpn(self.p,self.ir_poly,[other])
            elif isinstance(other,list):
                other = Fpn(self.p,self.ir_poly,other)
        return other
    def __add__(self,other):
        ' Addition über dem Körper F(p^n)'
        other = self.make_Fpn(other)
        if (self.p == other.p and self.ir_poly == other.ir_poly):
            result = [(self.value[i] + other.value[i]) % self.p for i in range(len(self.value))]
            return Fpn(self.p, self.ir_poly, result)
        else: print("ErRoR")
    def __sub__(self,other):
        ' Subtraktion über dem Körper F(p^n)'
        other = self.make_Fpn(other)
        result = Fpn(self.p,self.ir_poly,[other.p - x  for x in other.value])
        return(self + result)
    def invminus(self):
        ' gibt den Wert des Polynoms [0] - Vertreter zurück'
        return(Fpn(self.p,self.ir_poly,[0]) - self)
    def __mul__(self, other):
        ' Multiplikation über dem Körper F(p^n) ohne Kürzung mod irreduziblem Poynom'
        other = self.make_Fpn(other)
        n = len(self.value)
        result = [0] * (2 * n - 1)
        for i in range(n):
            for j in range(n):
                result[i+j] += self.value[i] * other.value[j]
        for i in range(2 * n - 1):
            result[i] %= self.p
        return Fpn(self.p,self.ir_poly, result)
    
    def div(self,value, other):
        ''' Argumente g(x) und h(x), gibt eindeutig bestimmtes q(x) und r(x) sodass g(x) = q(x) * h(x) + r(x) und degree(r(x)) < degree(h(x))
        Einfacher gesagt teilt es g(x) / h(x), gibt an wie oft Platz (q(x)) und Rest (r(x)) Polynome werden wieder als Liste dargestellt. Mithilfe von Polynomdivision über Fp'''
        if sum(other) == 0:
            print("division by Zero")
            return None
        while len(other)!= 0:
                if other[0] == 0:
                    other.pop(0)
                else: break
        while len(value)>= len(other):
                if value[0] == 0:
                    value.pop(0)
                else: break
        degree = len(other) - 1
        if len(value) < len(other):
            return ([0], value)
        floor = []
        while len(value) >= degree + 1:
            if value[0] == 0:
                value = value[1:]
                floor += [0]
            else:
                first_of_mod = Fp(value[0],self.p)
                facter = first_of_mod.invminus() / other[0]
                for i in range(degree + 1):
                    value[i] = ( value[i]  + (facter * other[i]).value) % self.p
                value = value[1:]
                floor += [self.p-facter.value]
        return [floor,value]
    
    def formate(self,value,ir_poly):
        'Vertreter der Klasse F(p^n) werden auf degree < n gebracht. Länger der Liste = n-1. Verwending des Restes mit der Methode div'
        if len(value) < self.degree:
            return (  [0] * (self.degree - len(value)) + value )
        elif len(value) == self.degree:
            return value
        else: return (self.div(value,ir_poly)[1])
    
    def __mod__(self, other):
        'r(x) der Methode div. Als Liste dargestellt'
        return (self.div(self.value,other)[1])
    
    def __floordiv__(self,value,other):
        'q(x) der Methode div. Als Liste dargestellt'
        return (self.div(value,other)[0])
    
    def __invert__(self):
        'gibt inverses Element eines Vertreters im Körper F(p^n) / ireduziblem Polynom an. Wird mit Hilfe des erweiterten Euklidischen Algorithmus für Polynome über Fp berechnet'
        a = copy.copy(self.ir_poly)
        b = copy.copy(self.value)
        c = []
        while sum(b) != 0:
            division = self.div(a,b)
            c += [Fpn(self.p, self.ir_poly, division[0])]
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
            print(a)
            print("nicht irreduzibel")
            return
        inv_a = (~Fp(a[0],self.p)).value   
        d = Fpn(self.p, self.ir_poly,[1])
        e = Fpn(self.p, self.ir_poly,[0])
        #d.print_value()
        #e.print_value()
        while c != []:
            temp = d
            d = e

            e = temp - c[-1] * e
            c.pop(-1)
        e.value = [(e.value[x] * inv_a ) % self.p for x in range(len(e.value))]
        #d.print_value()
        #e.print_value()
        return Fpn(self.p,self.ir_poly,e.value)
        #print(c)

    def __truediv__(self, other):
        ' Division über dem Körper F(p^n). Wird mit der Multiplikation des Inversen des Nenners berechnet'
        other = self.make_Fpn(other)
        return(self * (~other) )
    
    def __eq__(self,other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        if isinstance(other,Fpn):
            return (self.p == other.p and self.ir_poly == other.ir_poly and self.value == other.value)
        else: return False

    def __pow__(self,count):
        ' Wiederholte Multiplikation ( Potenz mit square and multiply. Laufzeit log(n))'
        result = Fpn(self.p,self.ir_poly,[1])
        counting = self
        while count > 0:
            if count % 2 == 1: result *= counting
            counting *= counting
            count = count // 2
        return result