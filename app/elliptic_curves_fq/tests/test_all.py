from ..src.endlicheKoerper_Fp import Fp
from ..src.endlicherKoerper_Fpn import Fpn
from ..src.elliptischeKurve import (curve, Points, curve_Fpn)

import unittest

class TestFp(unittest.TestCase):
    def test_addition(self):
        # Teste die Addition von Fp-Objekten
        a = Fp(3, 7)
        b = Fp(4, 7)
        c = a + b
        self.assertEqual(c, Fp(0, 7))
    
    def test_subtraction(self):
        # Teste die Subtraktion von Fp-Objekten
        a = Fp(3, 7)
        b = Fp(4, 7)
        c = a - b
        self.assertEqual(c, Fp(6, 7))
    
    def test_multiplication(self):
        # Teste die Multiplikation von Fp-Objekten
        a = Fp(3, 7)
        b = Fp(4, 7)
        c = a * b
        self.assertEqual(c, Fp(5, 7))
    
    def test_division(self):
        # Teste die Division von Fp-Objekten
        a = Fp(3, 7)
        b = Fp(4, 7)
        c = a / b
        self.assertEqual(c, Fp(6, 7))
    
    def test_power(self):
        # Teste die Potenzfunktion
        a = Fp(2, 7)
        b = a ** 3
        self.assertEqual(b, Fp(1, 7))

class TestFpn(unittest.TestCase):
    def test_addition(self):
        # Teste die Addition von Fpn-Objekten
        p = 7
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        a = Fpn(p, ir_poly, [4, 1])  # Erstelle Fpn-Objekt
        b = Fpn(p, ir_poly, [3, 2])
        c = a + b
        self.assertEqual(c, Fpn(p, ir_poly, [ 0, 3]))
    
    def test_subtraction(self):
        # Teste die Subtraktion von Fpn-Objekten
        p = 7
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        a = Fpn(p, ir_poly, [4, 1])  # Erstelle Fpn-Objekt
        b = Fpn(p, ir_poly, [3, 2])
        c = a - b
        self.assertEqual(c, Fpn(p, ir_poly, [1, 6]))
    
    def test_multiplication(self):
        # Teste die Multiplikation von Fpn-Objekten
        p = 7
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        a = Fpn(p, ir_poly, [4, 1])  # Erstelle Fpn-Objekt
        b = Fpn(p, ir_poly, [3, 2])
        c = a * b
        self.assertEqual(c, Fpn(p, ir_poly, [4,4]))
    
    def test_division(self):
        # Teste die Division von Fpn-Objekten
        p = 7
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        a = Fpn(p, ir_poly, [4, 1])  # Erstelle Fpn-Objekt
        b = Fpn(p, ir_poly, [3, 2])
        c = a / b
        self.assertEqual(c, Fpn(p, ir_poly, [2,0]))
    
    def test_power(self):
        # Teste die Potenzfunktion von Fpn-Objekten
        p = 7
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        a = Fpn(p, ir_poly, [4, 1])  # Erstelle Fpn-Objekt
        b = a ** 3
        self.assertEqual(b, Fpn(p, ir_poly, [4,2]))

class TestCurveAndPoints(unittest.TestCase):
    def test_curve_discriminante_is_zero(self):
        # Teste die Methode discriminante_is_zero der curve-Klasse
        p = 7
        a = [4,6]
        b = [5,2]
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        test_curve = curve_Fpn(a, b, p, ir_poly, [[6,6],[0,4]], None)  # Erstelle curve_Fpn-Objekt
        self.assertFalse(test_curve.discriminante_is_zero())  # Erwartet False
        
        # Ändern Sie a und b, um die Diskriminante zu 0 machen
        a = [0,0]
        b = [0,0]
        test_curve = curve_Fpn(a, b, p, ir_poly, [[0],[ 0]], None)  # Erstelle curve_Fpn-Objekt
        self.assertTrue(test_curve.discriminante_is_zero())  # Erwartet True
    
    def test_points_on_curve(self):
        # Teste die Methode on_Curve der Points-Klasse
        p = 7
        a = [4,6]
        b = [5,2]
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        test_curve = curve_Fpn(a, b, p, ir_poly, [[6,6],[0,4]], None)  # Erstelle curve_Fpn-Objekt
        point1 = Points([[6,6], [0,4]], test_curve)  # Punkt auf der Kurve
        self.assertTrue(point1.on_Curve())  # Erwartet True
        
        point2 = Points([[1,2],[5,2]], test_curve)  # Punkt nicht auf der Kurve
        self.assertFalse(point2.on_Curve())  # Erwartet False
    
    def test_point_addition(self):
        # Teste die Punktaddition in der Points-Klasse
        p = 7
        a = [4,6]
        b = [5,2]
        ir_poly = [1, 0, 1]  # Beispiel irreduzibles Polynom
        test_curve = curve_Fpn(a, b, p, ir_poly, [[6,6],[0,4]], None)  # Erstelle curve_Fpn-Objekt
        point1 = test_curve.startpoint
        result = point1 + point1
        self.assertTrue(result.on_Curve())

if __name__ == '__main__':
    unittest.main()




