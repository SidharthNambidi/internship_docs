
# AI Network Log Analyzer

## Overview
An AI-powered network log analyzer that uses the
Llama 3.1 8B model locally through Ollama to analyze
network payloads and identify potentially suspicious
patterns.

## Technologies Used
- Python
- Ollama
- Llama 3.1 8B
- Requests library

## Implementations

### 1. Python-based LLM Integration
A Python script accepts network payload strings,
sends them to the Llama 3.1 model through the Ollama
API, and displays a brief analysis.

### 2. Ollama Modelfile Customization
A customized Ollama model configuration with a
predefined system prompt for network log analysis.

## Setup Instructions

### 1. Install Ollama
https://ollama.com

### 2. Download the model
```bash
ollama pull llama3.1:8b
```

### 3. Clone this repository
```bash
git clone YOUR_REPOSITORY_URL
cd ai-network-log-analyzer
```

### 4. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Run the Python implementation
```bash
python3 main.py
```

### 7. Create the customized Ollama model
```bash
ollama create network-analyst -f Modelfile
```

### 8. Run the customized model
```bash
ollama run network-analyst
```

## Test Cases
- Normal GET request
- POST login request
- PUT and DELETE requests
- SQL injection pattern
- Directory traversal pattern
- Cross-site scripting pattern
- Command injection pattern

## Note
This is an experimental AI-based network payload
analysis project, made for learning. Its output is not a substitute
for a dedicated intrusion detection system.
