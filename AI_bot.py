from colorama import Fore, init
from openai import AzureOpenAI
import os
import subprocess
import json
import tiktoken


init(autoreset=True)

CHUNK_SIZE = 15000
MAX_CHUNKS = 20
text_loaded = False
text_content = None

class AI_bot:
    def __init__(self):
        self.chunks = []
        self.client = AzureOpenAI (
            azure_endpoint = os.getenv("AZURE_ENDPOINT"),
            api_key = os.getenv("API_KEY"),
            api_version = os.getenv("API_VERSION")
        )


    def count_tokens_in_file(self, file_path: str) -> int:
        model = "gpt-4o"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read file: {e}")

        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")  # fallback encoding

        tokens = encoding.encode(text)
        return len(tokens)


    def convert_txtfile_to_chunks(self, text_file_path):
        with open(text_file_path, "r", encoding="utf-8") as file:
            text_content = file.read()

        self.chunks = [text_content[i:i + CHUNK_SIZE] for i in range(0, len(text_content), CHUNK_SIZE)]
        self.chunks = self.chunks[:MAX_CHUNKS]


    # ------- Analyze & Summarize Interface -------
    def summary_tool(self):
        text_file_path = input("Which file would you like to analyze & summarize?\n")
        if not os.path.exists(text_file_path):
            raise FileNotFoundError(f"❌ File not found: {text_file_path}")
 
        # ---- Chop TXT File Into Chunks ----
        self.convert_txtfile_to_chunks(text_file_path)

        # ---- Summarize Each Chunk ----
        chunk_summaries = []
        print(f"\n📄 Summarizing {len(self.chunks)} chunks...\n")


        user_input = input("How technical would you like to your analysis to be?\n"
                "1 = Expert\n" 
                "2 = Moderate\n" 
                "3 = Easy\n")

        print("Your chosen input is: " + user_input + "\n")

        match user_input:
            case "1":
                convoSum = [({"role": "user", "content": "You are a cybersecurity expert in analyzing network traffic. You are assisting users who are experts in computer networking."})]
            case "2":
                convoSum = [({"role": "user", "content": "You are a cybersecurity expert in analyzing network traffic. You are assisting users with a moderate understanding of networking concepts."})]
            case "3":
                convoSum = [({"role": "user", "content": "You are a cybersecurity expert in analyzing network traffic. You are assisting users who have no technical background in networking."})]


        #convoSum = [{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files. You focus on malware and anomalies."}]

        for idx, chunk in enumerate(self.chunks, start=1):
            convoSum.append({"role": "user", "content": f"Summarize part {idx} of a PCAP text log:\n{chunk}"})
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=convoSum
            )
            summary = response.choices[0].message.content.strip()
            convoSum.append({"role": "assistant", "content": summary})
            chunk_summaries.append(f"Summary of Part {idx}:\n{summary}")
            print(f"✅ Chunk {idx}/{len(self.chunks)} summarized.\n")
            print(summary)

        # ---- Request Final Summary ----
        convoSum.append({"role": "user", "content": "Here are summaries of each part of a PCAP file:\n\n" + "\n\n".join(chunk_summaries)})
        convoSum.append({"role": "user", "content": "Based on the above summaries, give a short high-level summary of this PCAP file."})


        final_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=convoSum
        )

        final_summary = final_response.choices[0].message.content.strip()
        convoSum.append({"role": "assistant", "content": final_summary})

        print("\n🧠 Final Summary:\n")
        print(final_summary + "\n")

        print("Do you have any more questions?")
        while True:
            print("")
            print(Fore.CYAN + "You: ")
            user_input = input()
            if user_input.lower() in ["quit", "break"]: break
            convoSum.append({"role": "user", "content": user_input})

            response2 = self.client.chat.completions.create(
            model="gpt-4o",
            messages=convoSum
            )

            answer = response2.choices[0].message.content.strip()
            convoSum.append({"role":  "assistant", "content": answer})
            print(answer)

   # ------- Suricata Interface -------
    def suricata_tool(self):
        text_file_path = input("Which txt file would you like to use for context?\n")
        if not os.path.exists(text_file_path):
            raise FileNotFoundError(f"❌ File not found: {text_file_path}")
        
        with open(text_file_path, "r") as file:
            text_file = file.read()

        convoSuricata =[{"role": "system", "content": "You are a cybersecurity expert specializing in analyzing network traffic from PCAP and JSON files. You also have in-depth knowledge of Suricata and aim to assist users in writing and refining Suricata detection rules."}]
        convoSuricata.insert(0, {
            "role": "system", 
            "content": f"Context from from file: {text_file}"})
        
        while True:
            print("")
            print(Fore.CYAN + "You: ")
            user_input = input()
            if user_input.lower() in ["quit", "break"]: break

            convoSuricata.append({"role":"user", "content": user_input})
            
            chat = self.client.chat.completions.create(
                model="gpt-4o",
                messages=convoSuricata
            )

            answer = chat.choices[0].message.content.strip()
            convoSuricata.append({"role": "assistant", "content": answer})
            print(answer)

    # ---------- NMAP Interface ----------- #
    def nmap_tool(self):
        print("You are now speaking with an AI assistant specialized in Nmap scanning and operational technology (OT) networks.")
        convoNmap = [{"role": "system", "content": "You have expert knowledge of Nmap and understand how to safely use it on operational technology (OT) networks without causing disruption."}]

        while True:
            print("")
            print(Fore.CYAN + "You: ")
            user_input = input()
            if user_input.lower() in ["quit", "break"]: break

            convoNmap.append({"role":"user", "content": user_input})
            
            chat = self.client.chat.completions.create(
                model="gpt-4o",
                messages=convoNmap
            )

            answer = chat.choices[0].message.content.strip()
            convoNmap.append({"role": "assistant", "content": answer})
            print(answer)
