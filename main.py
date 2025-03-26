import argparse
import openai
import subprocess
import os
import sys
import colorama
from colorama import Fore
import pyfiglet

# Initialiseer colorama
colorama.init(autoreset=True)

def print_welcome_message():
    """Print een ASCII-titel en kleurrijke welkomstboodschap."""
    ascii_title = pyfiglet.figlet_format("REC-OT", font="slant")
    print(Fore.CYAN + ascii_title)
    print(Fore.YELLOW + "Welkom bij de OT Netwerk Tool 🚀✨")
    print(Fore.GREEN + "[INFO] Kies een optie uit het onderstaande menu")

def run_nmap_scan(target):
    """Voert een voorzichtige Nmap-scan uit op het opgegeven netwerk ip."""
    try:
        print(Fore.CYAN + f"[*] Voer een langzame Nmap-scan uit op {target}...")
        result = subprocess.run(["nmap", "-sS", "-T1", "--scan-delay", "5s", target], capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        return Fore.RED + "[ERROR] Nmap is niet geïnstalleerd of niet in PATH."
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"[ERROR] Nmap scan mislukt: {e}"

def analyze_pcap(pcap_file):
    """Analyseert een PCAP-bestand met Tshark."""
    if not os.path.exists(pcap_file):
        return Fore.RED + "[ERROR] PCAP-bestand niet gevonden."
    try:
        print(Fore.CYAN + f"[*] Analyseren van PCAP-bestand: {pcap_file}...")
        result = subprocess.run(["tshark", "-r", pcap_file], capture_output=True, text=True, check=True)
        return result.stdout[:1000]  # Beperk uitvoer voor leesbaarheid
    except FileNotFoundError:
        return Fore.RED + "[ERROR] Tshark is niet geïnstalleerd of niet in PATH."
    except subprocess.CalledProcessError as e:
        return Fore.RED + f"[ERROR] PCAP-analyse mislukt: {e}"

def chatgpt_analysis(prompt, api_key):
    """Genereert een AI-ondersteunde analyse via OpenAI."""
    if not api_key:
        return Fore.RED + "[ERROR] OpenAI API-key ontbreekt."
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Je helpt bij netwerkbeveiligingsanalyses."},
                      {"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        return Fore.RED + f"[ERROR] AI-analyse mislukt: {e}"

def show_kibana_dashboard():
    """Link naar Kibana-dashboard."""
    print("\n" + Fore.MAGENTA + "[INFO] Je kunt de resultaten visualiseren via Kibana op deze link:")
    print(Fore.MAGENTA + "http://localhost:5601")  # Pas dit aan afhankelijk van je eigen setup

def main():
    print_welcome_message()

    while True:
        print(Fore.YELLOW + "\n=======================")
        print(Fore.GREEN + "OT Netwerk Tools Menu")
        print(Fore.YELLOW + "=======================")
        print(Fore.CYAN + "1. 🚀 Voer een Nmap-scan uit")
        print(Fore.CYAN + "2. 📁 Analyseer een PCAP-bestand")
        print(Fore.CYAN + "3. 🤖 Vraag AI om netwerkadvies")
        print(Fore.CYAN + "4. 🌐 Toegang tot Kibana Dashboard")
        print(Fore.RED + "5. ❌ Stop")
        
        choice = input(Fore.WHITE + "\nMaak een keuze (1-5): ")

        if choice == "1":
            target = input(Fore.YELLOW + "Voer het doel-IP in voor de Nmap-scan: ")
            print(run_nmap_scan(target))

        elif choice == "2":
            pcap_file = input(Fore.YELLOW + "Voer het pad in naar het PCAP-bestand: ")
            print(analyze_pcap(pcap_file))

        elif choice == "3":
            prompt = input(Fore.YELLOW + "Wat wil je aan AI vragen? ")
            api_key = input(Fore.YELLOW + "Voer je OpenAI API-key in: ")
            print(chatgpt_analysis(prompt, api_key))

        elif choice == "4":
            show_kibana_dashboard()

        elif choice == "5":
            print(Fore.GREEN + "\n[INFO] Het programma wordt afgesloten...")
            break

        else:
            print(Fore.RED + "[ERROR] Ongeldige keuze. Probeer opnieuw.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[INFO] Script onderbroken door gebruiker.")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Onverwachte fout: {e}")
        sys.exit(1)
