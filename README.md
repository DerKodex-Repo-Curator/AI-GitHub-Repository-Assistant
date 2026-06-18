# AI GitHub Repository Assistant 🤖📁

**🌟 [Try the Live App Here!](https://ai-app-repository-assistant-f7bvnfzdstyehtwxbwscb8.streamlit.app/)**

AI GitHub Repository Assistant is a powerful tool built to analyze, chat with, and retrieve information from GitHub repositories using Retrieval-Augmented Generation (RAG). It allows users to input a GitHub repository and seamlessly ask questions about the codebase, documentation, and overall structure.

## 🚀 Features

* **Repository Loading:** Automatically fetches and processes repository files.
* **Intelligent Code Chunking:** Breaks down large codebases into manageable contexts.
* **Vector Embeddings & Storage:** Uses advanced embeddings and ChromaDB for fast, efficient vector search.
* **Groq LLM Integration:** Powered by Groq's blazing-fast inference for rapid, accurate responses.
* **Streamlit UI:** An intuitive, user-friendly web interface for chatting with the repository.

## 🛠️ Project Structure

* `src/app.py` / `src/ui.py`: Entry points for the Streamlit user interface.
* `src/loader.py`: Handles fetching and loading data from GitHub.
* `src/chunker.py`: Splits the retrieved code/text into smaller, semantic chunks.
* `src/embeddings.py`: Manages the generation of text embeddings.
* `src/vectorstore.py`: Interacts with ChromaDB to store and retrieve vectors.
* `src/retriever.py`: Fetches the most relevant document chunks based on user queries.
* `src/llm.py`: Connects to the Groq API for large language model generation.
* `src/chain.py`: Orchestrates the RAG pipeline (connecting the retriever to the LLM).

## ⚙️ Prerequisites

* Python 3.8+
* A [Groq API Key](https://console.groq.com/keys)


🛡️ License
This project is licensed under the MIT License.