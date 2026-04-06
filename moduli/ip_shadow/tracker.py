import os
import requests
import datetime
import sys
import time

# --- CONFIGURAZIONE ---
LOG_BASE_DIR = r"C:\Program Files\CyberShadow\moduli\ip_shadow\logs"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def colora(testo, colore="verde"):
    colori = {"verde": "\033[92m", "cyan": "\033[96m", "rosso": "\033[91m", "giallo": "\033[93m", "fine": "\033[0m"}
    if sys.platform != "win32":
        return f"{colori.get(colore, '')}{testo}{colori['fine']}"
    return testo

def print_logo():
    logo = r"""
      _____ _____   _____ _    _          _____   ______          __
     |_   _|  __ \ / ____| |  | |   /\   |  __ \ / __ \ \        / /
       | | | |__) | (___ | |__| |  /  \  | |  | | |  | \ \  /\  / / 
       | | |  ___/ \___ \|  __  | / /\ \ | |  | | |  | |\ \/  \/ /  
      _| |_| |     ____) | |  | |/ ____ \| |__| | |__| | \  /\  /   
     |_____|_|    |_____/|_|  |_/_/    \_\_____/ \____/   \/  \/    
                                                                    
      >> Network Untouchable // Identity Concealed // [ROOT ACTIVE] <<
    """
    print(colora(logo, "verde"))

def get_custom_log_name(directory):
    if not os.path.exists(directory):
        try: os.makedirs(directory)
        except: directory = "logs"
    counter = 1
    while True:
        nome_file = f"log{counter}111.txt"
        if not os.path.exists(os.path.join(directory, nome_file)): return os.path.join(directory, nome_file)
        counter += 1

def fetch_geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp", timeout=5)
        data = r.json()
        return f"{data['country']}, {data['city']} ({data['isp']})" if data.get('status') == 'success' else "Sconosciuto"
    except: return "Errore Connessione"

def main():
    ultimo_risultato = "" # Memorizza l'ultima ricerca per l'eventuale salvataggio
    ultimo_ip = ""

    while True:
        try:
            clear_screen()
            print_logo()
            
            # Se c'è stata una ricerca precedente, la mostra sopra il menu
            if ultimo_risultato:
                print("="*50)
                print(colora(f" ULTIMO TARGET: {ultimo_ip}", "cyan"))
                print(f" INFO         : {ultimo_risultato}")
                print("="*50 + "\n")

            # MENU SEMPRE VICINO
            print(colora("1) IP TO TRACK", "cyan"))
            print(colora("2) EXIT WITHOUT SAVING", "rosso"))
            print(colora("3) EXIT SAVING", "verde"))
            
            scelta = input("\n" + colora("IPSHADOW > ", "verde")).strip()

            if scelta == "1":
                ip = input(colora("\n[?] Inserisci IP: ", "giallo")).strip()
                if ip:
                    print(colora("[*] Analisi...", "verde"))
                    ultimo_ip = ip
                    ultimo_risultato = fetch_geo(ip)
                # Il ciclo ricomincia e pulisce, mostrando il risultato sopra le opzioni

            elif scelta == "2":
                print(colora("\n[!] Uscita in corso... Dati scartati.", "giallo"))
                time.sleep(1)
                break # Chiude il programma

            elif scelta == "3":
                if ultimo_risultato:
                    path = get_custom_log_name(LOG_BASE_DIR)
                    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(f"[{now}]\n")
                        f.write(f"ip1: {ultimo_ip} - {ultimo_risultato}\n")
                    print(colora(f"\n[V] Log salvato: {path}", "verde"))
                    time.sleep(2)
                else:
                    print(colora("\n[X] Nulla da salvare. Fai prima una ricerca!", "rosso"))
                    time.sleep(1.5)
                break # Chiude dopo il salvataggio

        except KeyboardInterrupt:
            # CTRL+C pulisce lo schermo e resetta
            ultimo_risultato = ""
            continue

if __name__ == "__main__":
    main()