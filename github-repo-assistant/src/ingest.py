import os
import shutil
import subprocess
import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from embeddings import embeddings

def process_github_repo(repo_url):
    """Clones a repo, clears locks, chunks multiple file types, and creates a Vector DB."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(base_dir, "..", "repo")
    db_path = os.path.join(base_dir, "..", "chroma_db")

    # 1. Clear system cache and old folders
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    # 2. Clone the new repository
    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    # 3. UPGRADE: Load multiple file types (Python, JS, TS, HTML, MD)
    extensions = ["**/*.py", "**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx", "**/*.html", "**/*.md"]
    docs = []
    for ext in extensions:
        loader = DirectoryLoader(repo_path, glob=ext, loader_cls=TextLoader)
        try:
            docs.extend(loader.load())
        except Exception:
            pass # Silently skip file types that cause decoding errors

    # 4. UPGRADE: Safety check to prevent empty list crashes
    if not docs:
        raise ValueError("No readable code files (Python, JS, HTML, MD) found in this repository.")

    # 5. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)

    if not chunks:
        raise ValueError("Files were found, but no text could be extracted.")

    # 6. Embed and store in ChromaDB
    Chroma.from_documents(chunks, embeddings, persist_directory=db_path)

    return len(docs), len(chunks)