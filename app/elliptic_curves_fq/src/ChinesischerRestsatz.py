# Python-Programm für den chinesischen Restsatz Algorithmus
def extended_gcd(a, b):
    'erweiterter Euklidischer Algoritmus'
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return [gcd, y - (b // a) * x, x]
 
def solve_for_a(Modules, Rests):
    'Liste von verschiedenen Modulos und eine andere List mit zugrhörigen Resten. die Zahl für welche dies alles zutrifft, wird hier berechnet'
    adds = []
    n = 1
    for i in Modules: 
        n *= i
    for count, i in enumerate (Modules):
        same = n // i
        inverses=extended_gcd(same,i)
        if inverses[1] > 0: 
            real = inverses[1]
        else: 
            real = inverses[1]%i
        adds += [(real * Rests[count] * same) % n]
    final = sum(adds) % n
    return final