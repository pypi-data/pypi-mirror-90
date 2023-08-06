.. raw:: html

    %path = "Mathe/Vektoren"
    %kind = chindnum["Texte"]
    %level = 11
    <!-- html -->

Wenn man die Zutaten von einer Auswahl von Kuchenrezepten als Vektorraum auffasst,
dann ist jeder Kuchen `z` ein Vektor im *Zutatenvektorraum*,
d.h. wir wählen unabhängig für jede Zutat (Variable `z_i`).
Wir verwenden den Wert 0, wenn die Zutat nicht verwendet wird.

Wenn man nur die Kuchen betrachtet,
dann ist eine Auswahl daraus ein Vektor `k` im *Kuchenvektorraum*.
Jedes `k_j` ist die Anzahl der Kuchensorte `j`.

Will man von einer Auswahl von Kuchen auf die Zutaten kommen,
dann ist das eine **Koordinatentransformation**.
Um die Gesamtmenge `z_i` zu erhalten muss man die Anzahl von jeder Kuchensorte `k_j`
mit der jeweiligen Zutatmenge multiplizieren.
Das läuft auf eine Matrixmultiplikation hinaus.

`z = ZK \cdot k = \sum_j ZK_{ij}k_j`

In `ZK` ist jede Spalte ein Rezept,
d.h. die Zutaten (**Komponenten**) für den Kuchen `j`.

Um auf den Preis `p` im *Preisvektorraum* zu kommen,
multiplizieren wir wieder

`p = PZ \cdot z = PZ_{1i} z_i`

`PZ` ist eine Matrix mit einer Zeile.
Die Anzahl von Zeilen ist die Dimension des Zielvektorraumes.

