from .elliptischeKurve import curve_Fpn, curve
from .endlicheKoerper_Fp import Fp
from .endlicherKoerper_Fpn import Fpn
import random
from .find_irreducible_polynomial import get_irreductible_polynomial


def get_randomcurve(p, n=1, should_print = True):
    '''generiert Zufällige Kurve über den Körper F(p^n). Im Fall n = 1 wird eine Kurve über F(p) erstellt. 
    Im Fall, dass das zweite Argument kein int mit dem Grad sondern eine Liste ist, 
    wird diese Liste als das irreduzible Polynom angenommen, und mithilfe diesem wird dann eine zfällige Kurve erstellt'''
    if isinstance(n,int):
        if n==1:
            x = random.randrange(p)
            y = random.randrange(p)
            a = random.randrange(p)
            temp_b = 0
            Kurve = curve(a,temp_b,p,[x,y],None)
            leftandright = Kurve.compute(x,y)
            b = (Fp(leftandright[0],p)-leftandright[1]).value
            Kurve = curve(a,b,p,[x,y],None)
            if Kurve.discriminante_is_zero():
                return get_randomcurve(p,n,should_print)
            if not Kurve.startpoint.on_Curve():
                print("Fehler beim erstellen.")
                return
            if should_print == True:            
                print("a = ", a)
                print("b = ", b)
                print("x = ", x)
                print("y = " ,y)
                print("Kurve wurde erfolgreich generiert. Hier die Kurve um abzuspeichern.")
                print(f"Kurve = curve({a},{b},{p},[{x},{y}],None)")
            return Kurve

        else:
            ir_poly = get_irreductible_polynomial(p,n)[0]
    else:
        ir_poly = n
    x =[]
    for i in range(len(ir_poly)-1):
        x += [random.randrange(p)]
    y =[]
    for i in range(len(ir_poly)-1):
        y += [random.randrange(p)]
    a =[]
    for i in range(len(ir_poly)-1):
        a += [random.randrange(p)]
    temp_b = [0]
    Kurve = curve_Fpn(a,temp_b,p,ir_poly,[x,y],None)
    leftandright = Kurve.compute(x,y)
    b = (Fpn(p, ir_poly, leftandright[0]) - Fpn(p, ir_poly,  leftandright[1])).value
    Kurve =(curve_Fpn(a,b,p,ir_poly,[x,y],None))
    if Kurve.discriminante_is_zero():
        return get_randomcurve(p,n,should_print)
    if not Kurve.startpoint.on_Curve():
        print("Fehler beim erstellen.")
        return
    if should_print == True:            
        print("irreduzibles Polynom = ", ir_poly)
        print("a = ", a)
        print("b = ", b)
        print("x = ", x)
        print("y = " ,y)
        print("Kurve wurde erfolgreich generiert. Hier die Kurve um abzuspeichern.")
        print(f"Kurve = curve_Fpn({a},{b},{p},{ir_poly},[{x},{y}],None)")
    return Kurve