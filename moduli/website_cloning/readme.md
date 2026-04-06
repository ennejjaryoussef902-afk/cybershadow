# CyberShadow - Website Cloning & Interception Module

Questo modulo fa parte del framework **CyberShadow** ed è progettato per il mirroring di siti web e l'intercettazione di dati (form, login, ricerche) a scopo di test di sicurezza e penetration testing.

## 🚀 Caratteristiche
- **Mirroring Istantaneo**: Clona l'interfaccia HTML/CSS di qualsiasi sito.
- **DNS Spoofing Locale**: Modifica automaticamente il file `hosts` per far apparire il sito su un dominio reale (es. `http://github.com`).
- **Data Interceptor**: Cattura i parametri GET e POST e li salva in tempo reale.
- **Auto-Redirect**: Reindirizza la vittima al sito originale dopo la cattura per minimizzare i sospetti.

## 🛠 Installazione
Assicurati di avere Python 3.11+ e le dipendenze installate:
```bash
pip install flask requests