import tiktoken
import os
from openai import AzureOpenAI

client = AzureOpenAI (
    azure_endpoint = os.getenv("AZURE_ENDPOINT"),
    api_key = os.getenv("API_KEY"),
    api_version = os.getenv("API_VERSION")
)

def split_text_file_by_token_limit(filepath, model="gpt-4o", max_tokens_per_chunk=10000):
    """
    Splits a large text file into chunks based on a token limit.

    :param filepath: Path to the large text file
    :param model: GPT model to base token encoding on (e.g., 'gpt-4o', 'gpt-3.5-turbo')
    :param max_tokens_per_chunk: Max tokens per chunk (default: 10,000)
    :return: List of text chunks
    """
    encoding = tiktoken.encoding_for_model(model)
    
    with open(filepath, "r") as file:
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

def send_chunks_to_gpt(chunks, client, model="gpt-4o", role="pcap"):
    """
    Sends text chunks to an OpenAI GPT model via chat completions.

    :param chunks: List of string chunks to process
    :param client: OpenAI or AzureOpenAI client instance
    :param model: Model name (e.g., 'gpt-4o')
    :param role: Type of task ('pcap', 'suricata', 'nmap')
    :return: List of model-generated responses per chunk
    """
    role_prompts = {
        "pcap": "You are a cybersecurity expert analyzing traffic logs from PCAP files.",
        "suricata": "You are an expert in Suricata and intrusion detection based on traffic patterns.",
        "nmap": "You are an expert in interpreting and recommending safe Nmap usage on OT networks."
    }

    convo = [{"role": "system", "content": role_prompts.get(role, "You are a helpful assistant.")}]
    responses = []

    for i, chunk in enumerate(chunks, start=1):
        print(f"\n🧠 Sending chunk {i}/{len(chunks)}...")

        convo.append({"role": "user", "content": f"Analyze this chunk:\n{chunk}"})

        try:
            chat = client.chat.completions.create(
                model=model,
                messages=convo
            )
            reply = chat.choices[0].message.content.strip()
            responses.append(reply)
            convo.append({"role": "assistant", "content": reply})
            print(f"✅ Chunk {i} processed.")
        except Exception as e:
            print(f"❌ Error on chunk {i}: {e}")
            responses.append(f"[ERROR] {str(e)}")

    return responses

chunks = split_text_file_by_token_limit("pcap_output.txt", model="gpt-4o")
responses = send_chunks_to_gpt(chunks, client, model="gpt-4o", role="pcap")
