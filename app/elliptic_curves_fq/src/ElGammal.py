from .Kurven import ord353
import random

'innit'
Kurve = ord353()
startpunkt = Kurve.startpoint
print(startpunkt)
'key generation'
privatekeya = random.randrange(Kurve.ord)
publickey_ga = startpunkt * privatekeya
'decrybtion'
message = random.randrange(100)
messagepoint = startpunkt * message
print(messagepoint)
r = random.randrange(Kurve.ord)
c0 = startpunkt * r
c1 = publickey_ga * r + messagepoint
'encribtion'
m = c0 * (Kurve.ord - privatekeya) + c1
print(m)