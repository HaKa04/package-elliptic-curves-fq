'implementation der Klasse F(2^n)'
import copy
class F2n:
    '''
    Python implementation des Endlichen Körpers F(2^n) mit der Primzahl 2, und einem ireduziblem Polynom Grad n
    '''
    def __init__(self, ir_poly, value):
        ' Konstruktor der Klasse mit irreduziblem Polynom über F2 als Liste, und Vertreter der Klasse, ebenfalls als Liste. Vetreter wird zuerst mit der Methode .formate gekürzt'
        self.ir_poly = ir_poly
        self.degree = len(ir_poly)-1
        self.value = self.formate(value,self.ir_poly)
        

    def print_value(self):
        ' Mit Printvalue, wird Vetreter als Liste ausgedrückt'
        print(self.value)

    def __add__(self, other):
        ' Addition über dem Körper F(2^n)'
        if self.ir_poly == other.ir_poly or len(self.value) != len(other.value):
            if not len(self.value)== len(other.value):
                if len(self.value) < len(other.value):
                    self.value = [0] * (len(other.value) - len(self.value)) + self.value
                elif len(other.value) < len(self.value):
                    other.value = [0] * (len(self.value) - len(other.value)) + other.value
            result = [(self.value[i] + other.value[i]) % 2 for i in range(len(self.value))]
            return F2n(self.ir_poly, result)
        else: print("ErRoR")
    def __sub__(self,other):
        ' Subtraktion über dem Körper F(2^n)'
        return(self + other)
    def __mul__(self, other):
        ' Multiplikation über dem Körper F(2^n) ohne Kürzung mod irreduziblem Poynom'
        n = len(self.value)
        result = [0] * (2 * n - 1)
        for i in range(n):
            for j in range(n):
                result[i+j] += self.value[i] * other.value[j]
        for i in range(2 * n - 1):
            result[i] %= 2
        return F2n(self.ir_poly, result)

    def div(self,value, other):
        ''' Argumente g(x) und h(x), gibt eindeutig bestimmtes q(x) und r(x) sodass g(x) = q(x) * h(x) + r(x) und degree(r(x)) < degree(h(x))
        Einfacher gesagt teilt es g(x) / h(x), gibt an wie oft Platz (q(x)) und Rest (r(x)) Polynome werden wieder als Liste dargestellt'''
        while len(other)!= 0:
                if other[0] == 0:
                    other.pop(0)
                else: break
        degree = len(other) - 1
        if len(value) < len(other):
            return ([0],value)
        floor = []
        while len(value) >= degree + 1:
            if value[0] == 0:
                value = value[1:]
                floor += [0]
            else:
                for i in range(degree + 1):
                    value[i] = (value[i] + other[i]) % 2
                value = value[1:]
                floor += [1]
        #print(floor)
        return [floor,value]
    
    def formate(self,value,ir_poly):
        'Vertreter der Klasse F(2^n) werden auf degree < n gebracht. Länger der Liste = n-1. Verwending des Restes mit der Methode div'
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
        'gibt inverses Element eines Vertreters im Körper F(2^n) / ireduziblem Polynom an. Wird mit Hilfe des erweiterten Euklidischen Algorithmus für Polynome über F2 berechnet'
        a = copy.copy(self.ir_poly)
        b = copy.copy(self.value)
        c = []
        while sum(b) != 0:
            division = self.div(a,b)
            c += [F2n(self.ir_poly, division[0])]
            while len(division[1])!= 0:
                if division[1][0] == 0:
                    division[1].pop(0)
                else: break
                
            a = b
            b = division[1]
        if a[-1] != 1 or sum(a) != 1 :
            print("nicht irreduzibel")
            return
            
        d = F2n(self.ir_poly,a)
        e = F2n(self.ir_poly,[0])
        #d.print_value()
        #e.print_value()
        while c != []:
            temp = d
            d = e

            e = temp - c[-1] * e
            c.pop(-1)
        #d.print_value()
        #e.print_value()
        return F2n(self.ir_poly,e.value)
        #print(c)
    def __truediv__(self, other):
        ' Division über dem Körper F(2^n). Wird mit der Multiplikation des Inversen des Nenners berechnet'
        return(self * (~other) )
    def __pow__(self,count):
        ' Wiederholte Multiplikation ( Potenz mit square and multiply. Laufzeit log(n))'
        result = F2n(self.ir_poly,[1])
        counting = self
        while count > 0:
            if count % 2 == 1: result *= counting
            counting *= counting
            count = count // 2
        return result
    def __eq__(self, other):
        'Gibt Bool zurück, ob zwei Elemente dieser Klasse Identisch sind. '
        return(self.ir_poly == other.ir_poly and self.value == other.value)

