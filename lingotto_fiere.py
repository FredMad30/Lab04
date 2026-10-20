from stand import Stand, StandPrese, StandPremium
from espositore import Espositore


class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self._stand = {}
        self._espositori = {}

    def get_nome(self):
        return self._nome

    def set_nome(self, nuovo_nome):
        if not nuovo_nome or not nuovo_nome.strip():
            raise ValueError("Il nome del centro fieristico non può essere vuoto.")
        self._nome = nuovo_nome.strip()

    def carica_file_dati(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for riga in file:
                    riga = riga.strip()
                    if not riga:
                        continue

                    campi = [c.strip() for c in riga.split(',')]
                    codice = campi[0]

                    if codice.startswith("ES") or len(campi) == 3:
                        cod_espositore, nome, cognome = campi[0], campi[1], campi[2]
                        espositore = Espositore(cod_espositore, nome, cognome)
                        self._espositori[cod_espositore] = espositore

                    elif codice.startswith("ST") or len(campi) >= 4:
                        cod_stand = campi[0]
                        superficie = float(campi[1])
                        padiglione = int(campi[2])
                        prezzo_base = float(campi[3])

                        if len(campi) == 4:
                            nuovo_stand = Stand(cod_stand, superficie, padiglione, prezzo_base)
                        else:
                            valore_extra = campi[4]
                            if valore_extra.isdigit():
                                nuovo_stand = StandPrese(cod_stand, superficie, padiglione, prezzo_base,
                                                         int(valore_extra))
                            else:
                                nuovo_stand = StandPremium(cod_stand, superficie, padiglione, prezzo_base, valore_extra)

                        self._stand[cod_stand] = nuovo_stand

        except FileNotFoundError:
            raise FileNotFoundError(f"Errore: il file '{file_path}' non è stato trovato.")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        if codice_stand not in self._stand:
            raise KeyError(f"Stand con codice '{codice_stand}' non trovato.")

        if codice_espositore not in self._espositori:
            raise KeyError(f"Espositore con codice '{codice_espositore}' non trovato.")

        stand = self._stand[codice_stand]
        espositore = self._espositori[codice_espositore]

        if not stand.get_disponibile():
            raise ValueError(f"Lo stand {codice_stand} è già assegnato a un altro espositore.")

        for st in self._stand.values():
            if st.espositore == espositore:
                raise ValueError(f"L'espositore {espositore.codice} ha già uno stand assegnato ({st.codice}).")

        stand.espositore = espositore

    def elenca_espositori(self):
        if not self._espositori:
            print("Nessun espositore presente nel sistema.")
            return

        for espositore in self._espositori.values():
            stand_associato = None
            for s in self._stand.values():
                if s.espositore == espositore:
                    stand_associato = s
                    break

            if stand_associato:
                print(
                    f"{espositore} -> Stand Assegnato: {stand_associato.codice} (Prezzo: {stand_associato.calcola_prezzo():.2f}€)")
            else:
                print(f"{espositore} -> Nessuno stand assegnato")

    def stand_ordinati_per_prezzo(self):
        return sorted(list(self._stand.values()))