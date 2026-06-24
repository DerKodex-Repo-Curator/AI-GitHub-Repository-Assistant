# 🛡️ AI DevSecOps Code Reviewer

**🌟 [Try the Live App Here!](https://ai-app-repository-assistant-f7bvnfzdstyehtwxbwscb8.streamlit.app/)**

The **AI DevSecOps Code Reviewer** is an end-to-end Retrieval-Augmented Generation (RAG) application engineered to act as a Senior Security Architect. By simply pasting a GitHub repository URL, the assistant dynamically clones the codebase, performs intelligent Abstract Syntax Tree (AST) parsing, and embeds the logic into a local vector database to conduct deep security and bug audits.

---

## 🚀 Key Features

* **🧠 AST-Level Parsing:** Utilizes Python's native `ast` module and LangChain's `Language` parsers to intelligently split code along function and class boundaries, ensuring logical context is never broken.
* **🛡️ Automated Security Audits:** Features a dedicated one-click review engine that scans the database for bugs, security vulnerabilities, code smells, and performance bottlenecks.
* **📥 Exportable Reports:** Instantly generate and download beautifully formatted Markdown (`.md`) audit reports to share with your engineering team.
* **100% Free Local Embeddings:** Utilizes `sentence-transformers` and the open-source `BAAI/bge-small-en-v1.5` model to generate embeddings entirely on your local machine.
* **Blazing Fast Inference:** Integrated with **Groq** to leverage the `Llama 3.1` model for near-instantaneous code analysis.
* **Premium Enterprise UI:** Features a custom Streamlit interface styled with a sleek GitHub Dark Mode aesthetic, dashboard metrics, and intuitive state management.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Custom CSS
* **Orchestration:** LangChain (LCEL)
* **Text Splitters:** Custom AST Extractor + RecursiveCharacterTextSplitter 
* **LLM Engine:** Groq (`llama-3.1-8b-instant`)
* **Embedding Model:** Hugging Face (`BAAI/bge-small-en-v1.5`)
* **Vector Database:** ChromaDB

---

## 💻 Local Installation & Setup

Want to run this DevSecOps assistant on your own machine? Follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/thakuryukti1-del/AI-GitHub-Repository-Assistant.git](https://github.com/thakuryukti1-del/AI-GitHub-Repository-Assistant.git)
cd AI-GitHub-Repository-Assistant


 2. Install dependencies
Ensure you have Python installed, then run:
pip install -r requirements.txt

3. Set up your Environment Variables
Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY="gsk_your_api_key_here"

4. Run the Application
Navigate to the src folder and start the Streamlit server:

Bash
streamlit run src/ui.py

📂 Project Structure
src/ui.py - The main Streamlit application and custom CSS front-end.

src/ingest.py - The data engine that clones repos, manages file locks, and executes syntax-aware multi-language chunking.

src/vectorstore.py / retriever.py - Manages the ChromaDB connection and document retrieval.

src/embeddings.py - Initializes the local Hugging Face embedding model.

src/llm.py - Connects to Groq's blazing-fast inference engine.

src/chain.py - The LCEL pipeline integrating the LLM, retriever, and conversational memory.
