from .Kurven import FBillionPowerTo20
import random
import time


TestKurve = FBillionPowerTo20()

Punkt_a = TestKurve.startpoint
#Punkt_a.x.print_value()

print(Punkt_a)
a = TestKurve.compute(Punkt_a.x,Punkt_a.y)
#print(a)
Punkt_b = Punkt_a * 2
#print(Punkt_b)
#print(TestKurve.compute(Punkt_b.x,Punkt_b.y))

ord = 10**(12*20)
a = random.randrange(TestKurve.a.p**20)
b = random.randrange(TestKurve.a.p**20)
start_proc = time.process_time()
key1 = (((Punkt_a*a)*b).x)
ende_proc = time.process_time()
print('Systemzeit: {:5.3f}s'.format(ende_proc-start_proc))
print(key1.value)
start_proc = time.process_time()
key2 = (((Punkt_a*b)*a).x)
ende_proc = time.process_time()
print('Systemzeit: {:5.3f}s'.format(ende_proc-start_proc))
print(key2.value)
print(key1==key2)
