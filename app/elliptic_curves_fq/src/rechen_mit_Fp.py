from .Kurven import P_192
import elliptischeKurve as eK
import math
import random


Ellip_Curve = P_192()
bound = Ellip_Curve.bound()


P = Ellip_Curve.startpoint

O = eK.Points("inf",Ellip_Curve)

a = random.randrange(bound[0])
b = random.randrange(bound[0])

key1 = (((P*a)*b).x)
print(key1)
key2 = (((P*b)*a).x)
print(key2)
print (P * P.Curve.ord)