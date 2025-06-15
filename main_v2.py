
# main_combined.py
import os
import sys
import platform
import subprocess
import webbrowser
import json
from colorama import Fore, init
from AI_bot import AI_bot  # ✅ Import your class from nmap.py

init(autoreset=True)


class MainApp:
    def __init__(self):
        self.ai_bot = AI_bot()
        self.token_limit = 128000

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

    def show_opensearch_dashboard(self):
        url = "https://145.52.127.172/dashboards/app/dashboards#/view/0ad3d7c2-3441-485e-9dfe-dbb22e84e576"
        print(Fore.GREEN + "[INFO] OpenSearch-dashboard wordt geopend in je browser...")
        webbrowser.open(url)


    # Read JSON File and write contents to TXT file
    def convert_json_to_txt(self, json_file_path, txt_file_path):
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"❌ File not found: {json_file_path}")
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                json.dump(data, txt_file, indent=4)  # Pretty-print JSON into txt

            print(f"✅ Converted '{json_file_path}' → '{txt_file_path}'.")

        except Exception as e:
            print(f"An error occurred: {e}")

    # ---- Convert PCAP to Plain Text using tshark ----
    def convert_pcap_to_txt(self, pcap_file_path, txt_file_path):
        if not os.path.exists(pcap_file_path):
            raise FileNotFoundError(f"❌ File not found: {pcap_file_path}")

        try:
            result = subprocess.run(
                ["tshark", "-r", pcap_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            with open(txt_file_path, "w") as f:
                f.write(result.stdout)

            print(f"✅ Converted {pcap_file_path} → {txt_file_path}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error converting PCAP: {e.stderr}")
            exit(1)


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
        print("1. OpenSearch Dashboard openen")
        print("2. Nmap commando's genereren (+ AI)")
        print("3. Suricata regels genereren (+ AI)")
        print("4. Netwerkverkeer analyseren & samenvatten (+ AI)")
        print("5. Calculate tokens of a txt file")
        print("6. Convert PCAP to TXT File")
        print("7. Convert JSON to TXT File")
        print("8. Check tools")
        print("9. Stop")

    def run(self):
        self.check_tools()

        while True:
            os.system("cls" if platform.system() == "Windows" else "clear")
            self.display_menu()

            choice = input(Fore.CYAN + " Maak een keuze (1-9): ")

            if choice == "1":
                self.show_opensearch_dashboard()

            elif choice == "2":
                print("Nmap Tool")
                self.ai_bot.nmap_tool()

            elif choice == "3":
                print("Suricata Tool")
                self.ai_bot.suricata_tool()                

            elif choice == "4":
                print("Analyse & Summary Tool")
                self.ai_bot.summary_tool()

            elif choice == "5":
                print("Give the name of the TXT file: ")
                user_input = input("")
                amount = self.ai_bot.count_tokens_in_file(user_input)
                print(f"The calculated tokens of the file is: {amount}\n")
                if amount > self.token_limit:
                    print("This file exceeds the token limit of gpt-4o, which is 128000")
                else:
                    print("This file doesn't exceed the token limit and can be used as input for the AI tools")

            elif choice == "6":
                print("Convert PCAP file to txt file")
                pcap_file_path = input("Give the name of the pcap file: ")
                if pcap_file_path.lower().endswith('.pcap'):
                    base_name = pcap_file_path[:-5]  # Removes last 5 characters
                else:
                    base_name = pcap_file_path

                txt_file_path = base_name + '.txt'
                self.convert_pcap_to_txt(pcap_file_path, txt_file_path)

            elif choice == "7":
                print("Convert JSON file to txt file")
                json_file_path = input("Give the name of the JSON file: ")
                if json_file_path.lower().endswith('.json'):
                    base_name = json_file_path[:-4]  # Removes last 5 characters
                else:
                    base_name = json_file_path

                txt_file_path = base_name + '.txt'
                self.convert_json_to_txt(json_file_path, txt_file_path)

            elif choice == "8":
                self.check_tools()

            elif choice == "9":
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
