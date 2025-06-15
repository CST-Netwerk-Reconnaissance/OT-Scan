from openai import AzureOpenAI
import os
import subprocess
import time

PCAP_FILE = "download ratexe truncated.pcap"
TEXT_FILE = "download ratexe truncated.txt"
PCAP_FILE2 = "download ratexe.pcap"
TEXT_FILE2 = "download ratexe.txt"
TEXT_FILE3 = "download big file.txt"
CHUNK_SIZE = 15000
MAX_CHUNKS = 20
text_loaded = False
text_content = None


client = AzureOpenAI (
    azure_endpoint = os.getenv("AZURE_ENDPOINT"),
    api_key = os.getenv("API_KEY"),
    api_version = os.getenv("API_VERSION")
)

with open(TEXT_FILE, "r", encoding="utf-8") as file:
    context_file = file.read()

with open(TEXT_FILE2, "r", encoding="utf-8") as file2:
    context_file2 = file2.read()

with open(TEXT_FILE3, "r", encoding="utf-8") as file3:
    context_file3 = file3.read()


   # ---- Convert PCAP to Plain Text using tshark ----
def convert_pcap_to_txt(pcap_path, txt_output_path):
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

def test():
    convo1 =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]
    convo1.append({"role":"user", "content":  "Give a short summary of maximum 15 lines"})
    convo1.insert(0, {
        "role": "system", 
        "content": f"Context from a pacp file: {context_file3}"})

    
    chat = client.chat.completions.create(
            model="gpt-4o",
            messages=convo1
        )

    answer = chat.choices[0].message.content.strip()
    print("\n answer 1 = " + answer + "\n")

    chat2 = client.chat.completions.create(
            model="gpt-4o",
            messages=convo1
        )

    answer = chat2.choices[0].message.content.strip()
    print("\n answer 2 = " + answer + "\n")

    chat3 = client.chat.completions.create(
            model="gpt-4o",
            messages=convo1
        )

    answer = chat3.choices[0].message.content.strip()
    print("\n answer 3 = " + answer + "\n")
    # convo2 =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]

    # convo2.insert(0, {
    #     "role": "system", 
    #     "content": f"Context from a pacp file: {context_file}"})


    
    # convo3 =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]

    # convo3.insert(0, {
    #     "role": "system", 
    #     "content": f"Context from a pacp file: {context_file}"})
    
    
    

  # ------- Suricata Interface -------
def convo_1():
    convo1 =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]

    convo1.insert(0, {
        "role": "system", 
        "content": f"Context from a pacp file: {context_file}"})
    
    while True:
        print("")
        user_input = input("You: ")
        if user_input.lower() in ["quit", "break"]: break

        convo1.append({"role":"user", "content":  user_input})
        
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=convo1
        )

        answer = chat.choices[0].message.content.strip()
        convo1.append({"role": "assistant", "content": answer})
        print(answer)

def convo_2():
    print("convo2")
    convo2 =[{"role": "system", "content": "You are an cybersecurity expert in analyzing network traffic from PCAP files, you as well have knowledge of Suricata."}]

    convo2.insert(0, {
        "role": "system", 
        "content": f"Context from multiple chunks of a file: {context_file}"})
    
    while True:
        print("")
        user_input = input("You: ")
        if user_input.lower() in ["quit", "break"]: break

        convo2.append({"role":"user", "content": user_input})
        
        chat = client.chat.completions.create(
            model="gpt-4o",
            messages=convo2
        )

        answer = chat.choices[0].message.content.strip()
        convo2.append({"role": "assistant", "content": answer})
        print(answer)

test()
#convo_1()
# time.sleep(10)
# convo_2()
#convert_pcap_to_txt(PCAP_FILE2, TEXT_FILE2)