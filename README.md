# 🧩 AI GitHub Repository Assistant 

**🌟 [Try the Live App Here!](https://ai-app-repository-assistant-f7bvnfzdstyehtwxbwscb8.streamlit.app/)**

The **AI GitHub Repository Assistant** is an end-to-end Retrieval-Augmented Generation (RAG) application that acts as your AI pair programmer. By simply pasting a GitHub repository URL, the assistant dynamically clones, chunks, and embeds the codebase into a local vector database, allowing you to ask complex questions and get code-backed answers instantly.

---

## 🚀 Key Features

* **Dynamic Repository Ingestion:** Paste any public GitHub URL directly into the UI to instantly clone and process the codebase.
* **Intelligent File Parsing:** Automatically traverses directories to extract and chunk source code (`.py`, `.js`, `.md`, `.html`, etc.) while gracefully handling read errors.
* **100% Free Local Embeddings:** Utilizes `sentence-transformers` and the open-source `BAAI/bge-small-en-v1.5` model to generate embeddings entirely on your local machine—no OpenAI API key required.
* **Conversational Memory:** Powered by LangChain's `RunnableWithMessageHistory`, the assistant remembers previous questions and context for a seamless chat experience.
* **Blazing Fast Inference:** Integrated with **Groq** to leverage the `Llama 3.1` model for near-instantaneous token generation.
* **Premium Custom UI:** Features a custom Streamlit interface styled with a sleek GitHub Dark Mode aesthetic, custom chat bubbles, and session management.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Custom CSS
* **Orchestration:** LangChain (LCEL)
* **LLM Engine:** Groq (`llama-3.1-8b-instant`)
* **Embedding Model:** Hugging Face (`BAAI/bge-small-en-v1.5`)
* **Vector Database:** ChromaDB

---

## 💻 Local Installation & Setup

Want to run this assistant on your own machine? Follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/AI-GitHub-Repository-Assistant.git](https://github.com/your-username/AI-GitHub-Repository-Assistant.git)
cd AI-GitHub-Repository-Assistant

### 2. Install Dependencies
Ensure you have Python installed, then run:
pip install -r requirements.txt

### 3.Set up your Environment Variables
Create a .env file in the root directory and add your Groq API key:
GROQ_API_KEY="gsk_your_api_key_here"

### 4.Run the Application
Navigate to the src folder and start the Streamlit server:
streamlit run src/ui.py


📂 Project Structure
src/ui.py - The main Streamlit application and custom CSS front-end.

src/ingest.py - The data engine that safely clones repos, manages file locks, and chunks code.

src/vectorstore.py / retriever.py - Manages the ChromaDB connection and document retrieval.

src/embeddings.py - Initializes the local Hugging Face embedding model.

src/llm.py - Connects to Groq's blazing-fast inference engine.

src/chain.py - The LCEL pipeline integrating the LLM, retriever, and conversational memory.

