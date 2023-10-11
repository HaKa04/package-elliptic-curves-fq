from .getrandomcurve import get_randomcurve
from .elliptischeKurve import curve_Fpn, Points
import time
import math

def laufzeit_i(Kurve, i):
    startpunkt = Kurve.startpoint
    inf = Points("inf", Kurve)
    start_proc = time.process_time()
    for i in range(i):
        inf += startpunkt
    ende_proc = time.process_time()
    return ende_proc-start_proc

def laufzeit_q (Kurve,q):
    startpunkt = Kurve.startpoint
    start_proc = time.process_time()
    startpunkt *= q 
    ende_proc = time.process_time()
    return ende_proc-start_proc


def laufzeit_prim(p1,p2,n):
    Kurve = get_randomcurve(p1,n,"no")
    Kurve2= get_randomcurve(p2,n,"no")
    a = (laufzeit_q(Kurve,Kurve.q))
    b = (laufzeit_q(Kurve2,Kurve2.q))


    print(a,b,a/b, math.log(p1)/math.log(p2))
    print(math.log(a/b,math.log(p1)/math.log(p2)))



def laufzeit_degree(n1,n2,p):
    Kurve = get_randomcurve(p,n1,"no")
    Kurve2= get_randomcurve(p,n2,"no")
    a = (laufzeit_q(Kurve,Kurve.q))
    b = (laufzeit_q(Kurve2,Kurve2.q))
    print(a,b,a/b,n1/n2)
    print(math.log(a/b,n1/n2))


p1= 999999999999989
p2 = 131
n = 5
laufzeit_prim(p1,p2,n)
p = 999983
n1 = 29
n2 = 8
laufzeit_degree(n1,n2,p)


