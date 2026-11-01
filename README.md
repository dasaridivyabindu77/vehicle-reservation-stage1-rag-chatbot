# vehicle-reservation-stage1-rag-chatbot
# Vehicle Reservation RAG Chatbot

A working, local-first parking reservation assistant built with Flask, Chroma, and SQLite.

## Features

- Grounded answers from static knowledge stored in Chroma.
- Live availability and pricing read from SQLite.
- Step-by-step reservation collection and confirmation.
- Input guardrails for credentials, personal data, and prompt-injection markers.
- Evaluation suite with retrieval Recall@K, Precision@K, latency, and response checks.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app.main
```

Open `http://127.0.0.1:5000`.

## Test and evaluate

```powershell
python -m pytest -q
python -m app.evaluate
```

The application stores dynamic data in `data/chatbot.db` and vectors in `data/chroma/`.