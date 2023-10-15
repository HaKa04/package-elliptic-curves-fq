import random
import math
import copy
'Methoden der Ver- und Entschlüsselung für die Menezes-Vanstone Verschlüsselung für die Anwendung im Bezug zu einer Speziellen Kurve'
def Menezes_Vanstone_encrybtion(message, curve, publickey):
    'Verschlüsselung'
    encrypted = []
    keys = []
    for i in message:
        if curve.ord != None:
            zi = random.randrange(curve.ord) # int
        else: 
            zi = random.randrange(curve.q) # int
        keys.append(zi)
        Ri = curve.startpoint * zi # Point
        Si = publickey * zi #Point
        Ti = [Si.x * i[0], Si.y * i[1] ] # List
        encrypted.append( [Ri, Ti])
    return [encrypted, keys]


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

def ordlist(text):
    'kreirt Liste mit 8 Elementen vom String'
    L= []
    for i in range(8):
        L.append(ord(text[i]))
    return(L)


def text_to_ascii(text):
    'Wandelt text in ascii Nummer um und ordnet sie in Listen von 8 Charactern zusammen. Immer zwei Listen kreiren eine grössere Liste. Solche zweidimensionale Listen werden bis zum Schluss des Textes kreirt.'
    splitted = [[]]
    for i in range(math.ceil((len(text)) / 16) + 1):
        for j in range(2):
            if i == j == 0:
                binzahl = str(len(text))
                binzahl = "0" * (16 - len(binzahl)) + binzahl
                part1 = binzahl[0:8]
                part2 = binzahl[8::]
                splitted[0] += [part1] + [part2]
            elif i == 0:
                continue
            else:
                if len(splitted)-1 == i: 
                    if len(text) >= 8:
                        splitted[i] += [text[0:8]]
                    else: 
                        if text != "":
                            splitted[i] += [text[0::] + chr(45) * (8- len(text))]
                            text = ""
                        else:
                            splitted[i] +=   [8 * chr(45)]
                else:
                    if len(text) >= 8:
                        #print(i,j)
                        #print(splited)
                        splitted.append([text[0:8]])
                    else: 
                        splitted.append([text[0::] + chr(45) * (8- len(text))])
                text = text[8::]
    splitted_as_string = copy.deepcopy(splitted)
    for i in range (len(splitted)):
        for j in range (2):
            splitted[i][j] = ordlist(splitted[i][j])
    return ( [splitted, splitted_as_string])
def ascii_to_text(message):
    'Wandelt Listen von Ascii Nummer in zugehörigen Charakter um und fusioniert alles zu einem Text'
    text = ""
    for i in message:
        List = i.value
        for j in List:
            text += chr(j)
    binzahl = int(text[0:16])
    text = text[16:16+binzahl]
    return(text)

