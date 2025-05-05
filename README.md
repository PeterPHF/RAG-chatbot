# 🧠 Knowledge-Based RAG Chatbot

An end-to-end Retrieval-Augmented Generation (RAG) chatbot built with Streamlit. This system leverages scraped mental health data, processes and embeds it, and uses a combination of retrieval and generative models to provide accurate and context-aware responses.

---

## 📌 Features

- 🔍 **Web Scraping**: Automatically collects data from predefined mental health resources.
- 🧹 **Data Cleaning & Chunking**: Cleans and breaks down large texts into manageable, meaningful chunks.
- 🧠 **Embedding & Indexing**: Transforms text chunks into vector embeddings and indexes them using FAISS for fast retrieval.
- 🗣️ **Retrieval-Augmented Generation**: Retrieves relevant context and feeds it into a language model to generate informed responses.
- 💬 **Streamlit Interface**: User-friendly chatbot interface for seamless interactions.

---

## 🗂️ Project Structure

rag_chatbot/
│
├── data/
│   ├── raw/                  # Original scraped data
│   │   └── Data.csv
│   ├── processed/            # Cleaned and chunked data
│   │   ├── cleaned_chunks.txt
│   │   └── chunks_with_metadata.json
│   └── embeddings/           # Vector representations
│       ├── chunk_embeddings.npy
│       └── data_index.faiss
│
├── src/
│   ├── data_collection/      # Web scraping scripts
│   │   ├── scraper.py
│   │   └── sources.json      # List of URLs to scrape
│   │
│   ├── preprocessing/        # Data cleaning and chunking
│   │   ├── cleaner.py
│   │   └── chunker.py
│   │
│   ├── embedding/            # Embedding generation
│   │   ├── embedder.py
│   │   └── faiss_indexer.py
│   │
│   ├── rag/                 # Core RAG functionality
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── rag_system.py    # Combines retriever + generator
│   │
│   └── app/                 # User interface
│       ├── app.py           # Streamlit/Flask app
│       └── static/          # CSS/images if needed
│
│
├── notebooks/               # Jupyter notebooks for exploration
│   ├── data_exploration.ipynb
│   └── model_testing.ipynb
│
├── requirements.txt         # Python dependencies
├── README.md                # Project overview
└── .gitignore

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/PeterPHF/RAG-chatbot.git
cd rag_chatbot
```

## 2.Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the App

```bash
cd src/app
streamlit run app.py
```

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙋‍♂️ Acknowledgements

FAISS by Facebook AI

OpenAI & Hugging Face for LLM APIs

Streamlit for interactive UI

Your mental health data sources
