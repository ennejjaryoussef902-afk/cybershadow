# CyberShadow 🛡️
**CyberShadow** è un framework modulare di CyberSecurity scritto in Python per Windows. Permette di testare tecniche di IP Tracking, Website Mirroring e analisi di rete in un ambiente controllato.

## 🚀 Funzionalità
* **Shadow Flask IP**: Server Flask integrato per catturare IP e dati form in tempo reale.
* **IP Shadow Tracker**: Geolocalizzazione IP e gestione log incrementali (`ip.txt`, `ip2.txt`).
* **Website Mirroring**: Clonazione istantanea di siti web per test di phishing etico.
* **Utility Suite**: Generazione Hash (MD5/SHA256), Port Scanner e integrazione GitHub.

## 📂 Struttura del Progetto
```text
/
├── cybershadow.py        # Terminale principale
├── moduli/
│   ├── ip_shadow/        # Logica di tracciamento
│   └── website_cloning/  # Motore di mirroring e log
└── requirements.txt      # Dipendenze (flask, requests)