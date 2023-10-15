from .Kurven import Ascii
import random
'Methoden der Ver- und Entschlüsselung für die Menezes-Vanstone Verschlüsselung'

def Menezes_Vanstone_encrybtion(message, curve, publickey):
    'Verschlüsselung'
    decrypted = []
    for i in message:
        if curve.ord != None:
            zi = random.randrange(curve.ord) # int
        else: 
            zi = random.randrange(curve.q) # int
        Ri = curve.startpoint * zi # Point
        Si = publickey * zi #Point
        Ti = [Si.x * i[0], Si.y * i[1] ] # List
        decrypted.append( [Ri, Ti])
    return decrypted


def Menezes_Vanstone_decrybtion(decrypted, curve, privatekey):
    'Entschlüsselung'
    message = []
    for i in decrypted:
        Ri = i[0]
        Ti = i[1]
        Si = Ri * privatekey
        messagepart_i = [Ti[0] / Si.x, Ti[1] / Si.y]
        message+=messagepart_i
    return message

'innit'
Kurve = Ascii()
startpunkt = Kurve.startpoint

'key generation'
if Kurve.ord != None:
    privatekeya = random.randrange(Kurve.ord)
else: 
    privatekeya = random.randrange(Kurve.q)

publickey_ga = startpunkt * privatekeya

'decribtion'

decrypted = Menezes_Vanstone_encrybtion([[[3,4,5],[2,1,3]],[[2,1,1],[6,6,0]]],Kurve,publickey_ga)
#print(decrypted)

encrypted = Menezes_Vanstone_decrybtion(decrypted, Kurve, privatekeya)
print(encrypted)