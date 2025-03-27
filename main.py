import subprocess
import platform
import os
import sys
import colorama
import webbrowser
from colorama import Fore

# Initialiseer colorama
colorama.init(autoreset=True)

# def print_welcome_message():
#     """Print een hardcoded ASCII-titel en kleurrijke welkomstboodschap."""
#     ascii_title = """
#   ____  _____ ____       ___ _____ 
#  |  _ \| ____/ ___|     / _ \_   _|
#  | |_) |  _|| |   _____| | | || |  
#  |  _ <| |__| |__|_____| |_| || |  
#  |_| \_\_____\____|     \___/ |_|  
                                   
#     """
#     print(Fore.CYAN + ascii_title)
#     print(Fore.YELLOW + "Welkom bij de OT Netwerk Tool 🚀✨")
#     print(Fore.GREEN + "[INFO] Kies een optie uit het onderstaande menu")

def is_installed(command):
    """Controleer of een programma geïnstalleerd is."""
    try:
        subprocess.run([command, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return False

def install_linux_tools():
    """Installeer Nmap en Tshark op Linux via APT/YUM."""
    try:
        if os.path.exists("/usr/bin/apt-get"):
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "nmap", "tshark"], check=True)
        elif os.path.exists("/usr/bin/yum"):
            subprocess.run(["sudo", "yum", "install", "-y", "nmap", "wireshark"], check=True)
        print(Fore.GREEN + "✅ Installatie voltooid!")
    except Exception as e:
        print(Fore.RED + f"❌ Installatie mislukt: {e}")

def check_tools():
    """Controleert of Nmap en Tshark geïnstalleerd zijn en vraagt of de gebruiker ze wil installeren."""
    nmap_installed = is_installed("nmap")
    tshark_installed = is_installed("tshark")

    if nmap_installed and tshark_installed:
        print(Fore.GREEN + "✅ Nmap en Tshark zijn al geïnstalleerd!")
    else:
        print(Fore.RED + "⚠️ Nmap of Tshark ontbreekt op dit systeem.")
        keuze = input(Fore.CYAN + "❓ Wil je deze installeren? (ja/nee): ").strip().lower()
        if keuze == "ja":
            install_linux_tools()
        else:
            print(Fore.RED + "⚠️ Installatie overgeslagen.")

def show_kibana_dashboard():
    """Open Kibana-dashboard in de standaard webbrowser."""
    url = "https://145.52.127.172/dashboards/app/dashboards#/view/0ad3d7c2-3441-485e-9dfe-dbb22e84e576"  # Pas deze link aan indien nodig
    
    print("\n" + Fore.GREEN + "[INFO] Kibana-dashboard wordt geopend in je browser...")
    
    webbrowser.open(url)  # Opent de URL in de standaard webbrowser

def nmap_scan(target, agressiviteit):
    """Voer een netwerk in kaart-brengende Nmap-scan uit op het opgegeven doel met verschillende agressiviteitsniveaus."""
    print(Fore.CYAN+ f"Scannen van netwerk {target} voor actieve apparaten met agressiviteit: {agressiviteit}...")

    # Bepaal de juiste Nmap-opdrachten op basis van de gekozen agressiviteit
    if agressiviteit == "1":  # Zachte scan
        nmap_command = ["nmap", "-sn", target]  # Ping-scan (geen poorten scannen)
    elif agressiviteit == "2":  # Normale scan
        nmap_command = ["nmap", "-sS", target]  # SYN-scan voor poorten
    elif agressiviteit == "3":  # Agressieve scan
        nmap_command = ["nmap", "-A", target]  # Agressieve scan (versie, OS-detectie, scripts)
    elif agressiviteit == "4":  # Ultra agressieve scan
        nmap_command = ["nmap", "-T4", "-A", "-p-", target]  # Versneld, alle poorten, agressief
    else:
        print(Fore.RED + "[ERROR] Ongeldige keuze voor agressiviteit.")
        return

    try:
        result = subprocess.run(
            nmap_command,  # Voer de gekozen Nmap-opdracht uit
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )

        # Toon de resultaten van de Nmap-scan
        print(Fore.GREEN + result.stdout)

    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Fout bij het uitvoeren van Nmap: {e.stderr}")

def display_menu():
    ascii_title = """
             ____  _____ ____       ___ _____ 
            |  _ \| ____/ ___|     / _ \_   _|
            | |_) |  _|| |   _____| | | || |  
            |  _ <| |__| |__|_____| |_| || |  
            |_| \_\_____\____|     \___/ |_|  
                                   
    """
    print(Fore.CYAN + ascii_title)
    print(Fore.CYAN + "Welkom bij de REC-OT 🚀")

    """Toon het hoofdmenu."""
    print(Fore.CYAN + "\n                       ")
    print(Fore.CYAN + "Menu:")
    print(Fore.CYAN + "                          ")
    print(Fore.CYAN + "1. Breng netwerk in kaart met Nmap")
    print(Fore.CYAN + "2. Analyseer een PCAP-bestand met Malcolm")
    print(Fore.CYAN + "3. Toegang tot Kibana Dashboard")
    print(Fore.CYAN + "4. Controleer Nmap & Tshark installatie")
    print(Fore.RED + "5. Stop")

def main_menu():
    """Hoofdmenu voor de tool zonder elke keer opnieuw te printen."""
    while True:
        os.system("cls" if platform.system() == "Windows" else "clear")  # ✅ Scherm wissen vóór het menu
        
        display_menu()  # ✅ Menu tonen bij eerste keer
        
        choice = input(Fore.CYAN + "\nMaak een keuze (1-6): ")

        # if choice == "1":
        #     target = input(Fore.YELLOW + "Voer het doel-IP in voor de Nmap-scan: ")
        #     print(Fore.CYAN + f"[*] Simulatie: Nmap-scan op {target} (echte scan hier toevoegen)")

        if choice == "1":
            target = input(Fore.WHITE + "Voer het netwerk IP in voor de Nmap-scan (bijv. 192.168.1.0/24): ")
            print(Fore.CYAN + "                          ")
            print(Fore.CYAN + "1. Zachte scan (alleen actieve hosts)")
            print(Fore.CYAN + "2. Normale scan (poorten scannen)")
            print(Fore.CYAN + "3. Agressieve scan (OS-detectie, versies, scripts)")
            print(Fore.CYAN + "4. Ultra agressieve scan (alle poorten, snel, gedetailleerd)")
            print(Fore.CYAN + "                          ")
            agressiviteit = input(Fore.WHITE + "Kies een agressiviteitsniveau (1-4): ")

            nmap_scan(target, agressiviteit)  # Voer de Nmap-scan uit met het gekozen agressiviteitsniveau

        elif choice == "2":
            pcap_file = input(Fore.WHITE + "Voer het pad in naar het PCAP-bestand: ")
            print(Fore.CYAN + f"[*] Simulatie: Analyseren van PCAP-bestand {pcap_file} (echte analyse hier toevoegen)")

        elif choice == "3":
            show_kibana_dashboard()  # ✅ Kibana-dashboard openen zonder menu-herhaling

        elif choice == "4":
            check_tools()

        elif choice == "5":
            print(Fore.WHITE + "\n[INFO] Het programma wordt afgesloten...")
            break

        else:
            print(Fore.RED + "[ERROR] Ongeldige keuze. Probeer opnieuw.")

        input(Fore.CYAN + "\nDruk op Enter om terug te keren naar het menu...")  # ✅ Pauze vóór herhaling


if __name__ == "__main__":
    try:
        # Print de welkomstboodschap met hardcoded ASCII-art
        # print_welcome_message()

        print(Fore.CYAN + "Automatische OS-detectie...")
        os_type = platform.system()
        print(Fore.GREEN + f"Gedetecteerd besturingssysteem: {os_type}")

        # Direct controleren of alles werkt
        check_tools()

        # Start het hoofdmenu
        main_menu()
    
    except KeyboardInterrupt:
        print(Fore.RED + "\n[INFO] Script onderbroken door gebruiker.")
        sys.exit(0)
    
    except Exception as e:
        print(Fore.RED + f"[ERROR] Onverwachte fout: {e}")
        sys.exit(1)
