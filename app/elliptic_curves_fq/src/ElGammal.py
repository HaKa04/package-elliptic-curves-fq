from .Kurven import ord353
import random
'El Gammal verschlüsselung, aber nicht als Funktion sondern für eigene Tests'
'innit'
Kurve = ord353()
startpunkt = Kurve.startpoint
print(startpunkt)
'key generation'
privatekeya = random.randrange(Kurve.q)
publickey_ga = startpunkt * privatekeya
'decrybtion'
message = random.randrange(Kurve.q)
messagepoint = startpunkt * message
print(messagepoint)
r = random.randrange(Kurve.q)
c0 = startpunkt * r
c1 = publickey_ga * r + messagepoint
'encribtion'
m = c0 * c1 - c0 * privatekeya
print(m)