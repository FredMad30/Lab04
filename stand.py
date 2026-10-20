from espositore import Espositore

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.espositore = None

    def get_disponibile(self):
        return self.espositore is None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __str__(self):
        stato = "Disponibile" if self.get_disponibile() else f"Assegnato a {self.espositore.codice}"
        return (f"{self.codice}: Standard | {self.superficie:.0f} mq - "
                f"Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}")


class StandPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        stato = "Disponibile" if self.get_disponibile() else f"Assegnato a {self.espositore.codice}"
        return (f"{self.codice}: Prese Extra | {self.superficie:.0f} mq - "
                f"Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - "
                f"Prese aggiuntive: {self.numero_prese} - {stato}")


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.get_disponibile() else f"Assegnato a {self.espositore.codice}"
        return (f"{self.codice}: Premium ({self.posizione}) | {self.superficie:.0f} mq - "
                f"Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}")