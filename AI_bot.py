from openai import AzureOpenAI
import os
import subprocess

#PCAP_FILE = "download ratexe truncated.pcap"
PCAP_FILE = "download ratexe.pcap"
TEXT_FILE = "pcap_output.txt"
CHUNK_SIZE = 15000
MAX_CHUNKS = 20
text_loaded = False
text_content = None
file_path = "example.txt"

class AI_bot:
    def __init__(self):
        self.convoNmap = [{"role": "system", "content": "You know all about nmap and how it can be used on OT-networks without interruption"}]
        self.convoPCAP = [{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files. You focus on malware and anomalies."}]
        self.convoSuricata =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]
        self.chunks = []
        #self.chunksSuricata = []

        self.client = AzureOpenAI (
            azure_endpoint = os.getenv("AZURE_ENDPOINT"),
            api_key = os.getenv("API_KEY"),
            api_version = os.getenv("API_VERSION")
        )

    # ---- Convert PCAP to Plain Text using tshark ----
    def convert_pcap_to_txt(self, pcap_path, txt_output_path):
        if not os.path.exists(pcap_path):
            raise FileNotFoundError(f"❌ File not found: {pcap_path}")

        try:
            result = subprocess.run(
                ["tshark", "-r", pcap_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            with open(txt_output_path, "w") as f:
                f.write(result.stdout)

            print(f"✅ Converted {pcap_path} → {txt_output_path}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error converting PCAP: {e.stderr}")
            exit(1)

    def convert_txtfile_to_chunks(self):
        with open(TEXT_FILE, "r", encoding="utf-8") as file:
            text_content = file.read()

        self.chunks = [text_content[i:i + CHUNK_SIZE] for i in range(0, len(text_content), CHUNK_SIZE)]
        self.chunks = self.chunks[:MAX_CHUNKS]

    def summarize_pcap(self):
        # ---- Chop TXT File Into Chunks ----
        self.convert_txtfile_to_chunks()
        # ---- Summarize Each Chunk ----
        chunk_summaries = []
        print("\n📄 Summarizing chunks...\n")

        for idx, chunk in enumerate(self.chunks, start=1):
            self.convoPCAP.append({"role": "user", "content": f"Summarize part {idx} of a PCAP text log:\n{chunk}"})
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.convoPCAP
            )
            summary = response.choices[0].message.content.strip()
            self.convoPCAP.append({"role": "assistant", "content": summary})
            chunk_summaries.append(f"Summary of Part {idx}:\n{summary}")
            print(f"✅ Chunk {idx} summarized.")
            print(summary)

        # ---- Request Final Summary ----
        self.convoPCAP.append({"role": "user", "content": "Here are summaries of each part of a PCAP file:\n\n" + "\n\n".join(chunk_summaries)})
        self.convoPCAP.append({"role": "user", "content": "Based on the above summaries, give a short high-level summary of this PCAP file."})


        final_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.convoPCAP
        )

        final_summary = final_response.choices[0].message.content.strip()
        self.convoPCAP.append({"role": "assistant", "content": final_summary})

        print("\n🧠 Final Summary:\n")
        print(final_summary + "\n")

    # ------- Suricata Interface -------
    def suricata_tool(self):
        print("Suricata")
        self.convert_txtfile_to_chunks()
        convo = self.convoSuricata
        suricataChunks = self.chunks
        convo.insert(0, {
            "role": "system", 
            "content": "Context from multiple chunks of a file: " + "\n\n".join(suricataChunks)})
        
        while True:
            print("")
            user_input = input("You: ")
            if user_input.lower() in ["quit", "break"]: break

            convo.append({"role":"user", "content": user_input})
            
            chat = self.client.chat.completions.create(
                model="gpt-4o",
                messages=convo
            )

            answer = chat.choices[0].message.content.strip()
            convo.append({"role": "assistant", "content": answer})
            print(answer)


    # ------- PCAP Interface -------
    def summary_tool(self):
        print("Your PCAP File will be summarized now")
        self.summarize_pcap()

        print("Do you have any more questions?\n")
        while True:
            print("")
            user_input = input("You: ")
            if user_input.lower() in ["quit", "break"]: break
            self.convoPCAP.append({"role": "user", "content": user_input})

            response2 = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.convoPCAP
            )

            answer = response2.choices[0].message.content.strip()
            self.convoPCAP.append({"role":  "assistant", "content": answer})
            print(answer)


    # ---------- NMAP Interface ----------- #
    def nmap_tool(self):
        print("You have started a conversation with an AI specialized in Nmap")
        convo = self.convoNmap   

        while True:
            print("")
            user_input = input("You: ")
            if user_input.lower() in ["quit", "break"]: break

            convo.append({"role":"user", "content": user_input})
            
            chat = self.client.chat.completions.create(
                model="gpt-4o",
                messages=convo
            )

            answer = chat.choices[0].message.content.strip()
            convo.append({"role": "assistant", "content": answer})
            print(answer)


#     # ----------- MENU ------------- #
#     def main_menu(self):
#          while True:
#             print("\nMaak een keuze\n")
#             print("1 = nmap")
#             print("2 = summary pcap")
#             print("3 = suricata rules based on pcap")
#             print("4 == quit")
#             choice=input()
            

#             if choice == "1": self.nmap_tool()
#             if choice == "2": self.summary_tool()
#             if choice == "3": self.suricata_tool()
#             if choice == "4": break



# if __name__ == "__main__":
#     nmap = Nmap()
#     nmap.convert_pcap_to_txt(PCAP_FILE, TEXT_FILE)
#     nmap.main_menu()





