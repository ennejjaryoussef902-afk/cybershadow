# Network Sniffer & Port Scanner

Modulo di monitoraggio rete basato su Python e Scapy. Questo tool è progettato per intercettare pacchetti IP specifici e avviare scansioni automatiche sulle porte dei bersagli rilevati.

## Funzionalità
- **Monitoraggio Real-time**: Analizza il traffico di rete alla ricerca di IP sospetti (es. Baidu).
- **Auto-Scan**: Se rileva traffico verso l'IP `103.235.46.102`, avvia una scansione automatica delle porte comuni (80, 443, 8080, ecc.).
- **Integrazione**: Progettato per essere richiamato dal terminale protetto `kali.py`.

## Requisiti
- Python 3.x
- Npcap (per Windows) o Libpcap (per Linux)
- Scapy: `pip install scapy`

## Utilizzo
Puoi lanciarlo direttamente per test:
```bash
python sniffing.py
