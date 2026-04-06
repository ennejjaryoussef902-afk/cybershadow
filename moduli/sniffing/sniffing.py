import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import socket
import threading
from scapy.all import sniff, IP, TCP, UDP, ICMP

class SniffinShadowGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SniffinShadow - Device & Network Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")
        
        self.sniffing = False
        self.thread = None

        # --- STILE ---
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        style.map("Treeview", background=[('selected', '#0078d7')])

        # --- SEZIONE SUPERIORE: GESTIONE DISPOSITIVI ---
        dev_label = tk.Label(root, text="GESTIONE DISPOSITIVI (Interfacce di Rete)", bg="#1e1e1e", fg="#00ff00", font=("Courier", 12, "bold"))
        dev_label.pack(pady=5)

        self.dev_tree = ttk.Treeview(root, columns=("MAC", "IP", "Status"), height=5)
        self.dev_tree.heading("#0", text="Interfaccia")
        self.dev_tree.heading("MAC", text="MAC Address")
        self.dev_tree.heading("IP", text="Indirizzo IP")
        self.dev_tree.heading("Status", text="Stato")
        self.dev_tree.pack(fill="x", padx=10)
        self.load_interfaces()

        # --- SEZIONE CENTRALE: MONITOR WIRESHARK ---
        sniff_label = tk.Label(root, text="LIVE PACKET SNIFFER (Wireshark Style)", bg="#1e1e1e", fg="#00ff00", font=("Courier", 12, "bold"))
        sniff_label.pack(pady=10)

        self.pkt_tree = ttk.Treeview(root, columns=("Time", "Proto", "Source", "Dest", "Len"), show="headings")
        self.pkt_tree.heading("Time", text="Time")
        self.pkt_tree.heading("Proto", text="Protocol")
        self.pkt_tree.heading("Source", text="Source IP")
        self.pkt_tree.heading("Dest", text="Destination IP")
        self.pkt_tree.heading("Len", text="Length")
        
        self.pkt_tree.column("Time", width=100)
        self.pkt_tree.column("Proto", width=80)
        self.pkt_tree.pack(fill="both", expand=True, padx=10)

        # --- CONTROLLI ---
        ctrl_frame = tk.Frame(root, bg="#1e1e1e")
        ctrl_frame.pack(fill="x", pady=10)

        self.btn_start = tk.Button(ctrl_frame, text="START SNIFFING", command=self.toggle_sniff, bg="#28a745", fg="white", font=("Arial", 10, "bold"), width=20)
        self.btn_start.pack(side="left", padx=20)

        self.btn_clear = tk.Button(ctrl_frame, text="PULISCI LOG", command=lambda: self.pkt_tree.delete(*self.pkt_tree.get_children()), bg="#dc3545", fg="white", width=15)
        self.btn_clear.pack(side="right", padx=20)

    def load_interfaces(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        for name, addrs in interfaces.items():
            ip, mac = "N/D", "N/D"
            for addr in addrs:
                if addr.family == socket.AF_INET: ip = addr.address
                if addr.family == psutil.AF_LINK: mac = addr.address
            status = "UP" if stats[name].isup else "DOWN"
            self.dev_tree.insert("", "end", text=name, values=(mac, ip, status))

    def packet_handler(self, pkt):
        if IP in pkt and self.sniffing:
            import datetime
            t = datetime.datetime.now().strftime("%H:%M:%S")
            src, dst = pkt[IP].src, pkt[IP].dst
            proto = "TCP" if TCP in pkt else "UDP" if UDP in pkt else "ICMP" if ICMP in pkt else "IP"
            length = len(pkt)
            
            # Inserisce nella tabella (Thread-safe via root.after)
            self.root.after(0, lambda: self.pkt_tree.insert("", 0, values=(t, proto, src, dst, length)))

    def sniff_worker(self):
        try:
            sniff(prn=self.packet_handler, stop_filter=lambda x: not self.sniffing, store=0)
        except Exception as e:
            messagebox.showerror("Errore", f"Devi eseguire come AMMINISTRATORE!\n{e}")
            self.sniffing = False
            self.btn_start.config(text="START SNIFFING", bg="#28a745")

    def toggle_sniff(self):
        if not self.sniffing:
            self.sniffing = True
            self.btn_start.config(text="STOP SNIFFING", bg="#ffc107")
            self.thread = threading.Thread(target=self.sniff_worker, daemon=True)
            self.thread.start()
        else:
            self.sniffing = False
            self.btn_start.config(text="START SNIFFING", bg="#28a745")

if __name__ == "__main__":
    root = tk.Tk()
    app = SniffinShadowGUI(root)
    root.mainloop()