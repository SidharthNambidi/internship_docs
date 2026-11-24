import requests

print("======= AI Network Log Analyzer =======")
print("Enter your network payload below.")
print("Type END on a new line when finished.\n")

# Accept multiple lines of input
payload_lines = []

while True:
    line = input()
    if line.strip() == "END":
        break
    payload_lines.append(line)

payload = "\n".join(payload_lines)

if not payload.strip():
    print("No payload entered. Exiting.")
    exit()


prompt = f"""
You are an AI network log analyst.
Analyze the following network payload string for any unusual patterns and reply with a brief summary.

Network Payload:
{payload}

Instructions:
1. Identify the HTTP method, requested resource, protocol version, and host.
2. Identify any genuinely suspicious patterns.
3. Do not classify missing optional HTTP headers as suspicious by themselves.
4. Distinguish between unususal behaviour and confirmed malicious activity.
5. If no suspicious patterns are present, explicitly state that the request appears normal.
6. Do not invent information that is not present in the payload.

Provide a brief, structured summary.
"""

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.1:8b",
    "prompt": prompt,
    "stream": False
}

try:
    print("Sending network payload to Llama 3.1 8B...")

    response = requests.post(
        url,
        json=data,
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    print("\n========== AI ANALYSIS ==========")
    print(result["response"])
    print("===================================")

except requests.exceptions.RequestException as error:
    print("Error communicating with Ollama:", error)
