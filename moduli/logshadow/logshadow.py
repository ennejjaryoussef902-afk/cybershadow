import subprocess
import datetime
import os

def cattura_usb(device_id):
    """Esegue il logcat e scrive il file finale"""
    
    # Crea il nome file con data e ora
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_file = f"logshadow/sessione_{device_id}_{timestamp}.log"
    
    print(f"\033[94m[*] Apertura flusso dati verso: {nome_file}\033[0m")
    
    try:
        with open(nome_file, "w", encoding="utf-8") as f:
            # Intestazione file
            f.write(f"--- CYBERSHADOW USB DUMP ---\nDEVICE: {device_id}\nDATE: {datetime.datetime.now()}\n" + "-"*30 + "\n")
            
            # Avvio ADB
            processo = subprocess.Popen(
                ["adb", "-s", device_id, "logcat", "*:V"], 
                stdout=subprocess.PIPE, 
                text=True
            )

            print("\033[93m[!] Monitoraggio USB attivo. CTRL+C per salvare.\033[0m\n")
            
            for riga in processo.stdout:
                print(f"\033[97m{riga.strip()}\033[0m") # Mostra a video
                f.write(riga) # Scrive nel file
                f.flush()

    except KeyboardInterrupt:
        print(f"\n\033[92m[OK] Sessione salvata correttamente in logshadow.\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Errore nel file logshadow.py: {e}\033[0m")