# SuperiorInsight

**Conversational AI System for Superior University**

SuperiorInsight is a production-grade Retrieval-Augmented Generation (RAG) system purpose-built for Superior University. It enables students, faculty, and administrative staff to query complex institutional information — degree programs, fee structures, admission policies, scholarships, and campus facilities — through a natural language interface with sub-second response times.

---

## Table of Contents

- [Overview](#overview)
- [Technical Architecture](#technical-architecture)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Dataset](#dataset)
- [Limitations](#limitations)
- [Author](#author)

---

## Overview

Traditional university information portals require users to navigate fragmented documentation across multiple pages. SuperiorInsight consolidates over 4,750 pages of Superior University's digital ecosystem into a single intelligent retrieval layer, enabling accurate, contextual, and multilingual responses without hallucination.

The system is designed with strict domain grounding — it does not speculate beyond the provided knowledge base — and maintains conversational context across multi-turn interactions without topic bleeding.

---

## Technical Architecture

```
User Query
    |
    v
Query Translation Layer (Roman Urdu / Hindi -> English)
    |
    v
History-Aware Retriever
    |
    v
FAISS Vector Database  <---  HuggingFace Embeddings
    |
    v
Context Assembly
    |
    v
Llama-3.3-70B via Groq LPU
    |
    v
Structured Response
```

| Component | Technology |
|---|---|
| Backend Framework | Flask |
| Embedding Model | HuggingFace Sentence Transformers |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| Language Model | Llama-3.3-70B |
| Inference Engine | Groq LPU |
| Orchestration | LangChain |
| Frontend | HTML / CSS / JavaScript |
| Deployment Target | Render / Railway / Heroku |

---

## Key Features

**Retrieval-Augmented Generation**
All responses are grounded in retrieved source documents. The system does not generate information outside the indexed knowledge base.

**Multilingual Query Support**
Handles queries in English, Roman Urdu, and Roman Hindi. A translation layer normalizes non-English input before retrieval, ensuring consistent embedding-space alignment.

**History-Aware Retrieval**
A custom memory engine maintains conversational context across turns. The retriever reformulates follow-up questions using prior context, eliminating the need for users to repeat themselves.

**Context Bleeding Prevention**
Each conversational session operates within strict topic boundaries. Context from unrelated prior exchanges does not contaminate current retrieval.

**Groq LPU Inference**
Responses are generated using Groq's Language Processing Unit, delivering low-latency completions suitable for production environments.

**Domain-Locked Prompting**
A strict system prompt constrains the model to answer only from retrieved context, with a calibrated fallback for out-of-scope queries.

---

## Project Structure

```
SuperiorInsight/
|
|-- app.py                  # Flask application, RAG pipeline, API routes
|-- requirements.txt        # Python dependencies
|-- .env                    # Environment variables (not committed)
|
|-- faiss_index/            # Pre-built vector database (AI Brain)
|   |-- index.faiss
|   |-- index.pkl
|
|-- templates/
|   |-- index.html          # Chat interface
|
|-- static/
|   |-- style.css           # Frontend styles
|   |-- script.js           # Frontend logic
|
|-- README.md
```

---

## Installation

**Prerequisites**

- Python 3.10 or higher
- pip
- A valid Groq API key

**Steps**

```bash
# Clone the repository
git clone https://github.com/your-username/superiorinsight.git
cd superiorinsight

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The FAISS index must be present in the `faiss_index/` directory before running the application. If you are rebuilding the index from source documents, run the ingestion script separately.

---

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

---

## Deployment

**Render**

1. Push the repository to GitHub.
2. Create a new Web Service on Render.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.
5. Add `GROQ_API_KEY` as an environment variable under the service settings.

**Railway**

1. Connect the GitHub repository to a new Railway project.
2. Add the `GROQ_API_KEY` environment variable.
3. Railway will auto-detect the Flask application and deploy.

**Heroku**

1. Ensure a `Procfile` is present: `web: gunicorn app:app`
2. Deploy via the Heroku CLI or GitHub integration.
3. Set the config var: `heroku config:set GROQ_API_KEY=your_key`

---

## Dataset

The vector database was constructed from over 4,750 pages sourced from Superior University's official digital ecosystem, including:

- Undergraduate and postgraduate program catalogs
- Admission policy documents
- Fee structures and scholarship guidelines
- Campus facility information
- Faculty and departmental directories
- Academic calendar and examination regulations

All source material is institutional property of Superior University, Lahore.

---

## Limitations

- Responses are bounded by the indexed knowledge base. Information not present in source documents will not be retrieved.
- The system does not browse the internet or access live university portals.
- The FAISS index must be manually rebuilt if source documents are updated.
- Multilingual translation accuracy depends on query clarity; heavily colloquial or ambiguous input may reduce retrieval precision.

---

## Author

**Syed Tahir**
BS Artificial Intelligence — 4th Semester
Superior University, Lahore

---

*SuperiorInsight is an academic project developed for educational purposes. It is not an official product of Superior University.*