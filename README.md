# 🛡️ Guardian Angel
### Your Friendly Assistant for Safer Messages

Guardian Angel is a cyber-safety assistant that helps users identify potential warning signs in suspicious messages. It combines rule-based risk detection with a locally running AI model to explain risks and offer practical safety advice.

## Features

- **Message analysis:** Checks messages for common scam and phishing indicators.
- **Risk scoring:** Assigns a risk score and classifies messages as low, medium, or high risk.
- **Warning signs:** Highlights suspicious phrases such as unexpected OTP requests, prize claims, and requests for banking details.
- **Local AI explanations:** Uses Ollama with the Llama 3.2 1B model to generate safety explanations.
- **Chat assistant:** Answers questions about OTPs, online scams, and cyber safety.
- **Multilingual support:** Offers English, Hindi, and Punjabi language options.
- **Web interface:** Provides an interface for analyzing messages and chatting with Guardian Angel.
- **REST API:** Built with FastAPI and Pydantic.
- **Workflow automation:** Integrates with n8n through a webhook and HTTP Request node.
- **Automated testing:** Includes pytest tests and a message-dataset evaluation script.

## Technology Stack

- Python (tested with Python 3.14.4)
- FastAPI and Pydantic
- Ollama and Llama 3.2 1B
- HTML, CSS, and JavaScript
- pytest
- n8n and Docker

## Project Structure

```text
guardian-angel/
├── main.py
├── test_main.py
├── evaluate.py
├── test_messages.csv
├── README.md
└── static/
    └── index.html
```

## Prerequisites

- Python 3.10 or later
- Ollama installed and running
- The `llama3.2:1b` model downloaded in Ollama
- Docker Desktop, if you want to run the n8n workflow

## Setup

Open a terminal in your project directory. Create and activate a virtual environment if you have not already done so:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install fastapi uvicorn pydantic pytest httpx
```

Make sure Ollama is running and the model is available:

```bash
ollama pull llama3.2:1b
```

The project uses the Ollama API URL configured in `main.py` by default. If your Ollama installation uses a different address, configure the `OLLAMA_URL` environment variable accordingly.

## Run the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

Open the web interface:

- http://127.0.0.1:8000/

Open the interactive API documentation:

- http://127.0.0.1:8000/docs

## API Endpoints

### `GET /`

Serves the Guardian Angel web interface.

### `POST /analyze`

Analyzes a message and returns its risk score, risk level, warning signs, explanations, and available AI explanation.

Example request:

```json
{
  "message": "URGENT! Send your OTP immediately.",
  "language": "English"
}
```

Supported language values: `English`, `Hindi`, and `Punjabi`.

### `POST /chat`

Sends a message to the Guardian Angel chat assistant.

Example request:

```json
{
  "message": "How can I stay safe from OTP scams?",
  "language": "English"
}
```

## Run Tests

Run the automated test suite:

```bash
pytest -q
```

Check Python syntax:

```bash
python -m py_compile main.py
```

### Verified test results

- Automated tests: **16 passed**.
- Python syntax check: **passed**.

## Evaluate the Message Dataset

Run the dataset evaluation script:

```bash
python evaluate.py
```

The script evaluates predictions against the labels in `test_messages.csv` and reports classification metrics.

**Current result on the included dataset:**

- Total messages: 30
- Correct predictions: 30
- Accuracy: 100%
- Precision: 100%
- Recall: 100%
- True positives: 15
- True negatives: 15
- False positives: 0
- False negatives: 0

These results apply only to the current, small, selected dataset. They do not guarantee perfect detection of real-world scams or phishing messages.

## n8n Workflow Integration

The project integrates with an n8n workflow using a Webhook node and an HTTP Request node that sends the message to the FastAPI `/analyze` endpoint.

When running n8n in Docker, the API address used inside the container may differ from the address used by the browser. In this setup, the workflow uses the following address to reach FastAPI running on the host:

```text
http://host.docker.internal:8000/analyze
```

The published webhook was tested using a POST request. A suspicious OTP-and-prize message returned a high-risk classification with a risk score of 6, three warning signs, and a safety note.

To test the webhook from your terminal, use:

```bash
curl -X POST http://localhost:5678/webhook/guardian-angel \
  -H "Content-Type: application/json" \
  -d '{"message":"URGENT! Send your OTP to claim your prize."}'
```

The n8n container and FastAPI server must be running for this test to succeed.

## Safety Notice

Guardian Angel highlights possible warning signs; it cannot prove that a message is fraudulent or guarantee that a message is safe. Verify unexpected requests using an official contact method. Never share an OTP, password, or verification code with someone who contacts you unexpectedly.

## Verified Results

- Automated tests: 16 passed.
- Python syntax check: passed.
- Dataset evaluation: 30 out of 30 predictions correct on the selected dataset.
- Accuracy, precision, and recall: 100% on this dataset.

These results apply only to the selected dataset and do not guarantee real-world scam detection accuracy.

## n8n Integration

The published n8n webhook was tested with a suspicious OTP-and-prize message and returned a high-risk classification.

When n8n runs in Docker, its HTTP Request node connects to FastAPI at:

`http://host.docker.internal:8000/analyze`

The webhook endpoint is:

`http://localhost:5678/webhook/guardian-angel`
