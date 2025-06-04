
# main_combined.py
import os
import sys
import platform
import subprocess
import webbrowser
from colorama import Fore, init
from AI_bot import AI_bot  # ✅ Import your class from nmap.py

init(autoreset=True)


class MainApp:
    def __init__(self):
        self.ai_bot = AI_bot()

    def is_installed(self, command):
        try:
            subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    def install_linux_tools(self):
        try:
            if os.path.exists("/usr/bin/apt-get"):
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "nmap", "tshark"], check=True)
            elif os.path.exists("/usr/bin/yum"):
                subprocess.run(["sudo", "yum", "install", "-y", "nmap", "wireshark"], check=True)
            print(Fore.GREEN + "✅ Installatie voltooid!")
        except Exception as e:
            print(Fore.RED + f"❌ Installatie mislukt: {e}")

    def check_tools(self):
        nmap_installed = self.is_installed("nmap")
        tshark_installed = self.is_installed("tshark")

        if nmap_installed and tshark_installed:
            print(Fore.GREEN + "✅ Nmap en Tshark zijn al geïnstalleerd!")
        else:
            print(Fore.RED + "⚠️ Nmap of Tshark ontbreekt op dit systeem.")
            keuze = input(Fore.CYAN + "❓ Wil je deze installeren? (ja/nee): ").strip().lower()
            if keuze == "ja":
                self.install_linux_tools()
            else:
                print(Fore.RED + "⚠️ Installatie overgeslagen.")

    def show_kibana_dashboard(self):
        url = "https://145.52.127.172/dashboards/app/dashboards#/view/0ad3d7c2-3441-485e-9dfe-dbb22e84e576"
        print(Fore.GREEN + "[INFO] Kibana-dashboard wordt geopend in je browser...")
        webbrowser.open(url)

    def nmap_scan(self, target, agressiviteit):
        print(Fore.CYAN + f"Scannen van netwerk {target} met agressiviteit {agressiviteit}...")

        if agressiviteit == "1":
            cmd = ["nmap", "-sn", target]
        elif agressiviteit == "2":
            cmd = ["nmap", "-sS", target]
        elif agressiviteit == "3":
            cmd = ["nmap", "-A", target]
        elif agressiviteit == "4":
            cmd = ["nmap", "-T4", "-A", "-p-", target]
        else:
            print(Fore.RED + "❌ Ongeldige keuze voor agressiviteit.")
            return

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
            print(Fore.GREEN + result.stdout)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"Fout bij Nmap: {e.stderr}")

    def display_menu(self):
        ascii_title = """
                ____  _____ ____       ___ _____ 
                |  _ \| ____/ ___|     / _ \_   _|
                | |_) |  _|| |   _____| | | || |  
                |  _ <| |__| |__|_____| |_| || |  
                |_| \_\_____\____|     \___/ |_|  
                                    
        """
        print(Fore.CYAN + ascii_title)
        print(Fore.CYAN + "Welkom bij de REC-OT 🚀")
        print(Fore.CYAN + "==== OT Netwerk Tool ====")
        print("1. Nmap Scan (klassiek)")
        print("2. PCAP analyse via GPT")
        print("3. Suricata analyse via GPT")
        print("4. AI Nmap gesprek")
        print("5. Kibana Dashboard openen")
        print("6. Check tools")
        print("7. Stop")

    def run(self):
        self.check_tools()

        while True:
            os.system("cls" if platform.system() == "Windows" else "clear")
            self.display_menu()

            choice = input(Fore.CYAN + " Maak een keuze (1-7): ")

            if choice == "1":
                target = input("Netwerk IP (bijv. 192.168.1.0/24): ")
                print("""
                        1. Zacht
                        2. Normaal
                        3. Agressief
                        4. Ultra""")
                level = input("Kies agressiviteit (1-4): ")
                self.nmap_scan(target, level)

            elif choice == "2":
                #self.nmap_ai.convert_pcap_to_txt("download ratexe.pcap", "pcap_output.txt")
                #self.nmap_ai.summary_tool()
                print("pcap analyse")

            elif choice == "3":
                #self.nmap_ai.convert_pcap_to_txt("download ratexe.pcap", "pcap_output.txt")
                #self.nmap_ai.suricata_tool()
                print("suricata analyse")

            elif choice == "4":
                self.nmap_ai.nmap_tool()

            elif choice == "5":
                self.show_kibana_dashboard()

            elif choice == "6":
                self.check_tools()

            elif choice == "7":
                print("Tot ziens!")
                break

            else:
                print(Fore.RED + "❌ Ongeldige keuze.")

            input(Fore.CYAN + "Druk op Enter om verder te gaan...")


if __name__ == "__main__":
    try:
        app = MainApp()
        app.run()
    except KeyboardInterrupt:
        print(Fore.RED + "[INFO] Script onderbroken door gebruiker.")
        sys.exit(0)
    except Exception as e: 
        print(Fore.RED + f"[ERROR] Onverwachte fout: {e}")
        sys.exit(1)
