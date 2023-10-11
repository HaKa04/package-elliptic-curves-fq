'''Implementation Klasse Fp

''' 
class Fp:
    ''' Python implementation des Endlichen Körpers Fp mit der Primzahl p als Klasse
'''
    def __init__(self, value, p):
        ' Konstruktor der Klasse, input Vertreter der Restklasse als value und p der Primzahl der Restklasse '
        self.value = value % p
        self.p = p
    
    def __str__(self):
        ' bei print wird der Vertreter ausgegeben'
        return str(self.value)
    
    def __repr__(self):
        ' Print von Fp in einer Liste wird je Vetreter und p ausgedruckt'
        return f"Fp({self.value}, {self.p})"
    
    def __add__(self, other):
        ' Methode der Addition über dem Körper'
        if isinstance(other, Fp) and self.p == other.p:
            return Fp(self.value + other.value, self.p)
        elif isinstance(other, int):
            return Fp(self.value + other, self.p)
        else:
            raise TypeError(f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'")
    
    def __sub__(self, other):
        ' Methode der Subtraktion über dem Körper'
        if isinstance(other, Fp) and self.p == other.p:
            return Fp(self.value - other.value, self.p)
        elif isinstance(other, int):
            return Fp(self.value - other, self.p)
        else:
            raise TypeError(f"unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'")
    
    def invminus(self):
        ' gibt den Wert 0 - Vertreter, Sprich p - Vertreter'
        return (Fp(0,self.p) - self)
    def __mul__(self, other):
        ' Methode der Multiplikation über dem Körper'
        if isinstance(other, Fp) and self.p == other.p:
            return Fp(self.value * other.value, self.p)
        elif isinstance(other, int):
            return Fp(self.value * other, self.p)
        else:
            raise TypeError(f"unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
    
    def __truediv__(self, other):
        ' Methode der Division über dem Körper Mithilfe der Multiplikation von dem Inversem des Nenners'
        if isinstance(other, Fp) and self.p == other.p:
            if other.value == 0:
                raise ZeroDivisionError("division by zero")
            return self * (~other)
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError("division by zero")
            return self * (~Fp(other, self.p))
        else:
            raise TypeError(f"unsupported operand type(s) for /: '{type(self)}' and '{type(other)}'")
    
    def __eq__(self, other):
        ' Gibt Bool zurück, ob zwei Vertreter gleich sind'
        if isinstance(other, Fp) and self.p == other.p:
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other % self.p
        else:
            return False
    
    def __invert__(self):
        ' Berechnet Inverses eines Vertreters in seiner Restklasse. '
        if self.value == 0:
            raise ZeroDivisionError("division by zero")
        return Fp(pow(self.value, -1, self.p), self.p)
    

    def inverses(self):
        'Berechnet Inverses eines Vertreters in seiner Restklasse. Diese mit eigener Implementation des erweiterten Euklidischen Algorithmus. Sie ist jedoch langsamer als der Algorithmus von Python. Deswegen werde ich für die Anwendung schon die vorhandene nehmen.'
        if self.value == 0:
            raise ZeroDivisionError("division by zero")
        a = self.p
        b = self.value
        c=[]
        while b != 0:
            temp = a%b
            c += [a//b]
            a = b
            b = temp
        d=1
        e=0
        while c != []:
            temp = d
            d = e

            e = temp - c[-1] * e
            c.pop(-1)
        return e % self.p
    def __pow__(self,count):
        ' Wiederholte Multiplikation ( Potenz mit square and multiply. Laufzeit log(n))'
        result = Fp(1, self.p)
        counting = self
        while count > 0:
            if count % 2 == 1: result *= counting
            counting *= counting
            count = count // 2
        return result