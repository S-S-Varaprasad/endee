# Endee AI Java Assistant

A lightweight, purely local Retrieval-Augmented Generation (RAG) command-line application built specifically using the **Endee Vector Database**.

## Project Overview

This project demonstrates a practical AI application (RAG/Semantic Search) leveraging the performance of the [Endee Vector Database](https://github.com/endee-io/endee). It processes raw text data about the Java programming language, generates AI embeddings, and answers user queries interactively from the terminal.

## System Design

The architecture of this project focuses on a decoupled, simple design:
1. **Embedding Layer**: Uses `sentence-transformers` (`all-MiniLM-L6-v2`) locally to avoid external API dependencies.
2. **Vector Database**: Connects to an **Endee** server using the official Python SDK to store and semantically search high-dimensional (384) vectors.
3. **Generative AI Layer**: Uses a small, fast local LLM (`google/flan-t5-small`) via Hugging Face `transformers` to synthesize final answers from the retrieved context.

### Use of Endee Vector Database
Endee lies at the core of the AI workflow:
- The `ingest.py` script automatically creates a cosine-space index within the Endee database using `Precision.FLOAT32`.
- Endee stores the document representations (embeddings) along with their string contexts as metadata.
- The `search.py` utility queries the Endee index for the nearest semantic neighbors to dynamically pull relevant information into the LLM prompt.

## Setup Instructions

### 1. Mandatory GitHub Steps
Before executing the program, please assure you have followed the steps requested by the assignments team:
- **Star** the [Endee GitHub Repository](https://github.com/endee-io/endee)
- **Fork** the repository to your own personal GitHub account.
- **Clone** your fork to your personal computer.

### 2. Start the Endee Server
Use the provided `docker-compose.yml` file to spin up the Endee Vector Database locally on port `8080`.
```bash
docker-compose up -d
```

### 3. Install Python Dependencies
It is highly recommended to use a Python virtual environment.
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows
source venv/bin/activate       # On Mac/Linux
pip install -r requirements.txt
```

### 4. Build the Knowledge Base
Run the ingestion script. It will connect to Endee, chunk the `java_notes.txt` file, embed the chunks, and push the vectors into the database.
```bash
python ingest.py
```

### 5. Chat with the Application
Finally, start the interactive Terminal application.
```bash
python app.py
```
*Try asking: "What is Java?" or "Who developed Java originally?"*
