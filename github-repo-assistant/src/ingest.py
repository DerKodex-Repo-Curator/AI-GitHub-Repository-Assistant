import os
import shutil
import subprocess
import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.vectorstores import Chroma
from embeddings import embeddings

# 1. Map file extensions to LangChain's Language parsers
EXTENSION_MAPPING = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".jsx": Language.JS,
    ".ts": Language.TS,
    ".tsx": Language.TS,
    ".java": Language.JAVA,
    ".cpp": Language.CPP,
    ".go": Language.GO,
    ".rs": Language.RUST,
    ".html": Language.HTML,
    ".md": Language.MARKDOWN,
}

def process_github_repo(repo_url):
    """Clones a repo, clears locks, chunks multiple file types smartly, and creates a Vector DB."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(base_dir, "..", "repo")
    db_path = os.path.join(base_dir, "..", "chroma_db")

    chromadb.api.client.SharedSystemClient.clear_system_cache()
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

    # 2. Expanded file extensions list
    extensions = [
        "**/*.py", "**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx", 
        "**/*.java", "**/*.cpp", "**/*.go", "**/*.rs", 
        "**/*.html", "**/*.md", "**/*.yaml", "**/*.json"
    ]
    
    docs = []
    for ext in extensions:
        loader = DirectoryLoader(repo_path, glob=ext, loader_cls=TextLoader)
        try:
            docs.extend(loader.load())
        except Exception:
            pass 

    if not docs:
        raise ValueError("No supported code or text files found in this repository.")

    # 3. Dynamic splitting based on file language
    chunks = []
    for doc in docs:
        # Extract the file extension from the document metadata
        file_path = doc.metadata.get("source", "")
        _, ext = os.path.splitext(file_path)
        
        # Check if the extension has a dedicated syntax parser
        if ext in EXTENSION_MAPPING:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=EXTENSION_MAPPING[ext],
                chunk_size=1000,
                chunk_overlap=200
            )
        else:
            # Fallback to standard character splitting for YAML, JSON, etc.
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            
        # Split this single document and add to our master list
        chunks.extend(splitter.split_documents([doc]))

    if not chunks:
        raise ValueError("Files were found, but no text could be extracted.")

    Chroma.from_documents(chunks, embeddings, persist_directory=db_path)

    return len(docs), len(chunks)