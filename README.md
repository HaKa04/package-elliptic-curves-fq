# Bibliothek für elliptische Kurven

## Beschreibung :pencil:
Diese Bibliothek bietet Funktionalitäten für elliptische Kurven über endlichen Körpern $\mathbb{F}_{p^n}$. Sie ermöglicht unter anderem Berechnungen auf elliptischen Kurven.

## Verwendung :computer:
Um die Funktionalitäten dieser Bibliothek zu nutzen, können Sie die folgenden Schritte ausführen:

1. **Installation :inbox_tray::**
   Sie können die elliptische Kurven Bibliothek mit pip installieren:

   ```sh
   pip install elliptic-curves-fq
   ```

2. **Importieren des Paketes :box::**
   Hier wird gezeigt, wie man die Bibliothek verwenden kann. 

   ```python
   # Erforderliche Module importieren
   import elliptic_curves_fq
   ```

3. **Klassen und ihre Verwendung :gear::**

   - **Fp:** Stellt ein endlichen Körper $F_p$ bereit und unterstützt arithmetische Operationen wie Addition, Subtraktion, Multiplikation, Division und Potenzieren durch Überschreiben der vorhandenen Operationen von Python. 

     - **Parameter:**
       - `element` (int): Ein Element im endlichen Körper.
       - `p` (int): Eine Primzahl, die den endlichen Körper definiert.

     ```python
     from elliptic_curves_fq import Fp
     # Beispielcode für Fp
     p = 23
     element = Fp(7, p)
     print(element)  # Ausgabe: 7
     print(element + 20) # Ausgabe 4
     print(element - 10) # Ausgabe 20
     print(element ** 2) # Ausgabe 3
     ```
   - **get_irreductible_polynomial:** Erlaubt die Generierung eines irreduziblen Polynoms über einem endlichen Körper $\mathbb{F}_{p}$.

     - **Parameter:**
       - `p` (int): Die Primzahl, die den endlichen Körper definiert.
       - `n` (int): Der Grad des Polynoms.

     ```python
     from elliptic_curves_fq import get_irreductible_polynomial
     # Beispielcode für get_irreductible_polynomial
     p = 17
     n = 3
     poly, attempts = get_irreductible_polynomial(p, n)
     print(poly)  # Ausgabe: [1, 7, 1, 10]
     print(attempts)  # Ausgabe: 3 (Anzahl der Versuche, die benötigt wurden, um das irreduzible Polynom zu generieren.)
     ```

   - **Fpn:** Erlaubt das Rechnen mit endlichen Körpern $F_{p^n}$ und bietet Methoden wie Addition, Subtraktion, Multiplikation, Division und Potenzieren durch Überschreiben der vorhandenen Operationen von Python.

     - **Parameter:**
       - `p` (int): Eine Primzahl, die den endlichen Körper definiert.
       - `irreducible_poly` (list): Ein irreduzibles Polynom über dem endlichen Körper $\mathbb{F}_p$.
       - `element` (list): Ein Element im endlichen Körper.

     ```python
     from elliptic_curves_fq import Fpn
     # Beispielcode für Fpn
     p = 17
     irreducible_poly = [1, 1, 1, 2]  
     element = Fpn(p, irreducible_poly, [1, 2, 3]) 
     print(element)  # Ausgabe: [1, 2, 3]
     print(element + [5,4,3]) #Ausgabe [6, 6, 6]
     print(element * [2,1,3]) #Ausgabe [6, 2, 3]
     print(element ** 5) #Ausgabe [6, 7, 12]
     ```

   - **curve:** Ermöglicht die Arbeit mit elliptischen Kurven über endlichen Körpern $F_{p}$. Eine elliptische Kurve hat die folgende Form \[y^2 = x^3 + ax + b\]

     - **Parameter:**
       - `a` (int): Der Koeffizient 'a' der elliptischen Kurve.
       - `b` (int): Der Koeffizient 'b' der elliptischen Kurve.
       - `p` (int): Eine Primzahl, die den endlichen Körper definiert.
       - `start_point` (list): Ein Startpunkt auf der elliptischen Kurve.
       - `ord` (int): Die Ordnung der Kurve. Wenn die Ordnung nicht bestummen wurde: None
     - Die Koeffizienten a und b werden direkt zu Objekten der Klasse Fp gemacht. 

     ```python
     from elliptic_curves_fq import curve
     # Beispielcode für curve
     p = 17
     a = 12  
     b = 6  
     start_point = [8,11]  
     curve = curve(a, b, p, start_point, None)
     print(curve)  # Ausgabe: curve( a = 12, b = 6, p = 17, Startpoint = (8, 11), ord = None)
     ```

   - **curve_Fpn:** Ermöglicht die Arbeit mit elliptischen Kurven über endlichen Körpern $F_{p^n}$. 

     - **Parameter:**
       - `a` (list): Der Koeffizient 'a' der elliptischen Kurve.
       - `b` (list): Der Koeffizient 'b' der elliptischen Kurve.
       - `p` (int): Eine Primzahl, die die Basis für den endlichen Körper $\mathbb{F}_p$ ist.
       - `irreducible_poly` (list): Ein irreduzibles Polynom über dem $\mathbb{F}_p$, welches den Körper $\mathbb{F}_{p^n}$ definiert.
       - `start_point` (list): Ein Startpunkt auf der elliptischen Kurve.
       - `ord` (int): Die Ordnung der Kurve.
     - Die Koeffizienten a und b werden direkt zu Objekten der Klasse Fpn gemacht.
     ```python
     from elliptic_curves_fq import curve_Fpn
     # Beispielcode für curve_Fpn
     p = 17
     irreducible_poly = [1, 1, 1, 2]  
     a = [1, 12, 8]  
     b = [2, 7, 6]  
     start_point = [[9, 10, 11],[7, 2, 4]]  
     curve = curve_Fpn(a, b, p, irreducible_poly, start_point, None)
     print(curve)  # Ausgabe: curve_Fpn( a = [1, 12, 8], b =[2, 7, 6], p = 17, ir_poly = [1, 1, 1, 2], Startpoint = ([9, 10, 11], [7, 2, 4]), ord = None)
     ```

   - **get_random_curve :game_die::** Ermöglicht das Erstellen einer neuen zufälligen Kurve. 

     - **Parameter:**
       - `p` (int): Eine Primzahl, die den endlichen Körper definiert.
       - `degree` (int): Der Grad der Kurve.
       - `should_print` (bool): Ein Parameter, der bestimmt, ob die Kurve gedruckt werden soll.

     ```python
     from elliptic_curves_fq import get_random_curve
     # Beispielcode für get_random_curve
     p = 17
     degree = 7
     get_randomcurve(p,degree) # Ausgabe unter anderem: Kurve wurde erfolgreich generiert. Hier die Kurve um abzuspeichern. 
     # Kurve = curve_Fpn([15, 5, 14, 5, 3, 10, 16],[11, 10, 7, 8, 13, 4, 4],17,[1, 6, 14, 13, 4, 8, 13, 8],[[10, 15, 9, 13, 7, 2, 6],[6, 0, 12, 15, 2, 1, 12]],None)
     curve = get_randomcurve(p,degree,should_print=False)
     start_point = curve.startpoint 
     ```

   - **Points:** Ermöglicht die Arithmetik elliptischer Kurve und unterstützt Operationen wie Punktaddition, Punktvervielfachung und andere Funktionen im Kontext elliptischer Kurven. 

     - **Parameter:**
       - `curve` (object): Die elliptische Kurve, mit der der Punkt verbunden ist.
       - `point` (list): Ein Punkt auf der elliptischen Kurve.

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

   - **Gespeicherte Kurven :floppy_disk::**
      - **P_192:** Sichere NIST-Kurve über Fp mit p ungefähr 2^192
      - **FBillionPowerTo20:** Eigene Kurve über $F(p^n) $mit p ungefähr 1 Billion und n = 20.
      - **P991:** Eigene Kurve über $F(991^3)$. Die Parameter sind zufällig.
      - **P23:** Eigene Kurve über $F(23^3)$. Die Parameter sind zufällig.
      - **ord353:** Eigene Kurve über $F(7^3)$. Die Ordnung der elliptischen Kurve ist 353 und somit prim. Jeder Punkt ist ein Generator.
      - **testcurvemod5:** Eigene Kurve über $F(5^3)$.
      - **kurzmod5:** Eigene kleinste mögliche Kurve über $F(5^2)$.
      - **Ascii:** Eigene Kurve über $F(131^8)$.
      - **ten_power_12_power_150:** Eine spezielle Kurve mit extrem hohen Werten mit p ungefähr 1 Billion und n = 150

    Die Kurven sind als Funktionen abgespeichert. Jede Funktion hier hat kein Argument, und man erhält die zugehörige Kurve.
     ```python
     from elliptic_curves_fq import ord353
     #Beispiel Code
     Kurve = ord353()
     startpunkt = Kurve.startpoint
     ```

4. **Weitere Informationen :page_facing_up::**
   - Die vollständige Dokumentation für die Bibliothek finden Sie in meinem [GitHub](https://github.com/HaKa04/package-elliptic-curves-fq) Account im Odrner docs. 
   
## License :scroll:
Dieses Projekt steht unter der MIT License - Sehen sie unter LICENSE für Details nach.

Ich hoffe, dass Sie diese Bibliothek nützlich finden. Bitte zögern Sie nicht, bei Fragen oder Anregungen mich unter kaspar.hui@gmail.com zu kontaktieren.