import tiktoken
import os
import subprocess
from openai import AzureOpenAI

pcap_path = "download ratexe truncated.pcap"
txt_output_path = "download ratexe truncated.txt"
tokenLimit = 125000


# client = AzureOpenAI (
#     azure_endpoint = os.getenv("AZURE_ENDPOINT"),
#     api_key = os.getenv("API_KEY"),
#     api_version = os.getenv("API_VERSION")
# )

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

# step 1. encode, step 2. turn text into tokens  3. return length
def count_amount_of_tokens(txt_output_path) -> int:
    encoding = tiktoken.encoding_for_model("gpt-4o")

    with open(txt_output_path, "r", encoding="utf-8") as file:
        full_text = file.read()

    num_tokens = len(encoding.encode(full_text))

    return num_tokens


def split_text_file_by_token_limit(filepath, model="gpt-4o", max_tokens_per_chunk=20000):
    """
    Splits a large text file into token-limited chunks.
    """
    encoding = tiktoken.encoding_for_model(model)

    with open(filepath, "r", encoding="utf-8") as file:
        full_text = file.read()

    tokens = encoding.encode(full_text)
    total_tokens = len(tokens)

    chunks = []
    start = 0

    while start < total_tokens:
        end = min(start + max_tokens_per_chunk, total_tokens)
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end

    return chunks


def send_chunks_to_gpt(chunks, client, model="gpt-4o", role="pcap", batch_size=3):
    """
    Sends batches of text chunks to the GPT model as chat completions.
    """
    role_prompts = {
        "pcap": "You are a cybersecurity expert analyzing traffic logs from PCAP files.",
        "suricata": "You are an expert in Suricata and intrusion detection based on traffic patterns.",
        "nmap": "You are an expert in interpreting and recommending safe Nmap usage on OT networks."
    }

    convo = [{"role": "system", "content": role_prompts.get(role, "You are a helpful assistant.")}]
    responses = []

    batched_chunks = ["\n\n".join(chunks[i:i + batch_size]) for i in range(0, len(chunks), batch_size)]

    for i, batch in enumerate(batched_chunks, start=1):
        print(f"\n🧠 Sending batch {i}/{len(batched_chunks)}...")
        convo.append({"role": "user", "content": f"Analyze this data batch for malware and anomalies:\n{batch}"})

        try:
            chat = client.chat.completions.create(
                model=model,
                messages=convo
            )
            reply = chat.choices[0].message.content.strip()
            responses.append(reply)
            convo.append({"role": "assistant", "content": reply})
            print(f"✅ Batch {i} processed.")
            print("\n" + reply + "\n")
        except Exception as e:
            print(f"❌ Error on batch {i}: {e}")
            responses.append(f"[ERROR] {str(e)}")

    return responses

# chunks = split_text_file_by_token_limit("pcap_output.txt", model="gpt-4o")
# responses = send_chunks_to_gpt(chunks, client, model="gpt-4o", role="pcap")
#convert_pcap_to_txt(pcap_path, txt_output_path)

amount = (count_amount_of_tokens("download big file.txt"))


if amount > tokenLimit:
    print("\nFile exceeds the token limit for this model. Make the file smaller. The amount is :" + str(amount) + "\n")
else:
    print(amount)
    print("\n")

amount = (count_amount_of_tokens("download ratexe truncated.txt"))


if amount > tokenLimit:
    print("File exceeds the token limit for this model. Make the file smaller. The amount is :" + str(amount) + "\n")
else:
    print(amount)
    print("\n")
