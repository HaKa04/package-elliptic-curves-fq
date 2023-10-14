# Bibliothek für elliptische Kurven 

## Beschreibung
Diese Bibliothek bietet Funktionalitäten für elliptische Kurven über endlichen Körpern $\mathbb{F}_{p^n}$. Sie ermöglicht unter anderem Berechnungen auf elliptischen Kurven.

## Verwendung
Um die Funktionalitäten dieser Bibliothek zu nutzen, können Sie die folgenden Schritte ausführen:

1. **Installation:**
   Sie können die elliptische Kurven Bibliothek mit pip installieren:

   ```sh
   pip install elliptic-curves-fq
   ```

2. **Verwendung:**
   Hier wird gezeigt, wie man die Bibliothek verwenden kann. 

   ```python
   # Erforderliche Module importieren
   import elliptic_curves_fq
   ```

3. **Klassen und ihre Verwendung:**

   - **Fp:** Stellt ein endlichen Körper $F_p$ bereit und unterstützt arithmetische Operationen wie Addition, Subtraktion, Multiplikation, Division und Potenzieren durch Überschreiben der vorhandenen Operationen von Python. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import Fp

     # Beispielcode für Fp
     p = 23
     element = Fp(7, p)
     print(element)  # Ausgabe: 7
     print(element + 20) # Ausgabe 4
     print(element - 10) #Ausgabe 20
     print(element ** 2) #Ausgabe 3
     ```

   - **Fpn:** Erlaubt das Rechnen mit endlichen Körpern $F_{p^n}$ und bietet Methoden wie Addition, Subtraktion, Multiplikation, Division und Potenzieren durch Überschreiben der vorhandenen Operationen von Python. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import Fpn

     # Beispielcode für Fpn
     p = 17
     irreducible_poly = [1, 1, 1, 2]  # Beispiel für ein irreduzibles Polynom \(x^3 + x^2 + x + 2 $ über $\mathbb{F}_17\)
     element = Fpn(p, irreducible_poly, [1, 2, 3]) # Erstellt das Element x^2 + 2x + 3 in der Restklasse modulo x^3 + x^2 + x + 2
     print(element)  # Ausgabe: [1, 2, 3]
     print(element + [5,4,3]) #Ausgabe [6, 6, 6]
     print(element * [2,1,3]) #Ausgabe [6, 2, 3]
     print(element ** 5) #Ausgabe [6, 7, 12]
     ```
   - **curve:** Ermöglicht die Arbeit mit elliptischen Kurven über endlichen Körpern $F_{p}$. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import curve

     p = 17
     a = 12  # Beispielkoeffizienten für a
     b = 6  # Beispielkoeffizienten für b
     start_point = [8,11]  # Beispiel für den Startpunkt
     curve = curve(a, b, p, start_point, None)
     print(curve)  # Ausgabe: curve( a = 12, b = 6, p = 17, Startpoint = (8, 11), ord = None)
     ```
   - **curve_Fpn:** Ermöglicht die Arbeit mit elliptischen Kurven über endlichen Körpern $F_{p^n}$. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import curve_Fpn

     p = 17
     irreducible_poly = [1, 1, 1, 2]  # Beispiel für ein irreduzibles Polynom \(x^3 + x^2 + x + 2 $ über $\mathbb{F}_17\)
     a = [1, 12, 8]  # Beispielkoeffizienten für a
     b = [2, 7, 6]  # Beispielkoeffizienten für b
     start_point = [[9, 10, 11],[7, 2, 4]]  # Beispiel für den Startpunkt
     curve = curve_Fpn(a, b, p, irreducible_poly, start_point, None)
     print(curve)  # Ausgabe: curve_Fpn( a = [1, 2, 3], b =[2, 3, 4], p = 19, ir_poly = [1, 1, 1, 2], Startpoint = ([9, 10, 11], [7, 2, 4]), ord = None)
     ```
   - **get_random_curve:** Ermöglicht das Erstellen einer neuen zufälligen Kurve. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import get_randomcurve

     p = 17
     degree = 7
     get_randomcurve(p,degree) # Ausgabe unter anderem: Kurve wurde erfolgreich generiert. Hier die Kurve um abzuspeichern. 
     # Kurve = curve_Fpn([15, 5, 14, 5, 3, 10, 16],[11, 10, 7, 8, 13, 4, 4],17,[1, 6, 14, 13, 4, 8, 13, 8],[[10, 15, 9, 13, 7, 2, 6],[6, 0, 12, 15, 2, 1, 12]],None)
     curve = get_randomcurve(p,degree,should_print=False)
     start_point = curve.startpoint 
     # Wenn man die Kurve nutzen, aber nicht abspeichern will.
     
     ```

   - **Points:** Ermöglicht die Aretmetik elliptischer Kurve und unterstützt Operationen wie Punktaddition, Pubktverfielfachung und andere Funktionen im Kontext elliptischer Kurven. Hier ist ein Beispielcode:

     ```python
     from elliptic_curves_fq import Points, curve_Fpn

     curve = curve_Fpn([1, 12, 8], [2, 7, 6], 17, [1, 1, 1, 2], [[9, 10, 11],[7, 2, 4]], None)  # Beispielkurve
     point = curve.startpoint 
     point2 = Points([[3, 12, 16], [1, 4, 13]],curve) 

     print(point)  # Ausgabe: ([9, 10, 11], [7, 2, 4])
     print(point2) # Ausgabe: ([3,12,16],[1,4,13])
     print(point + point2 ) # Ausgabe ([12, 8, 1], [1, 0, 5])
     print(point * 3500) #Ausgabe ([8, 8, 2], [11, 11, 2])
     ```

4. **Weitere Informationen:**
   - Die vollständige Dokumentation für die Bibliothek finden Sie in meinem [GitHub](https://github.com/HaKa04/package-elliptic-curves-fq) Account im Odrner docs. 
   
Ich hoffe, dass Sie diese Bibliothek nützlich finden. Bitte zögern Sie nicht, bei Fragen oder Anregungen mich unter kaspar.hui@gmail.com zu kontaktieren.
