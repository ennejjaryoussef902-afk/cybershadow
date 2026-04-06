import os

def cerca_match_deHasing(hash_da_cercare):
    """
    Cerca un hash SHA-256 nel database locale e restituisce il valore originale.
    """
    # Individua la cartella dove si trova questo script
    cartella_modulo = os.path.dirname(__file__)
    file_database = os.path.join(cartella_modulo, "deHasing.txt")

    # Verifica se il file .txt esiste
    if not os.path.exists(file_database):
        return "[!] Errore: File deHasing.txt non trovato nella cartella."

    # Pulizia dell'input
    hash_da_cercare = hash_da_cercare.strip().lower()

    try:
        with open(file_database, "r") as f:
            for riga in f:
                # Salta righe vuote o malformate
                if ":" not in riga:
                    continue
                
                hash_salvato, valore_chiaro = riga.strip().split(":", 1)
                
                if hash_salvato.lower() == hash_da_cercare:
                    return valore_chiaro
                    
    except Exception as e:
        return f"[!] Errore di lettura: {e}"

    return None

if __name__ == "__main__":
    print("--- CYBERSHADOW ANALYZER (deHasing) ---")
    h_input = input("Inserisci l'hash da decodificare: ").strip()
    
    if h_input:
        risultato = cerca_match_deHasing(h_input)
        if risultato:
            print(f"[+] Corrispondenza trovata: {risultato}")
        else:
            print("[-] Nessun match trovato nel database locale.")
    else:
        print("[!] Input non valido.")