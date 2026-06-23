import os
import shutil
import subprocess
import ast
import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from embeddings import embeddings

# Map file extensions to LangChain's Language parsers
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

def extract_python_ast_chunks(doc: Document):
    """Uses Python's native AST to perfectly extract Classes, Functions, and Imports."""
    chunks = []
    code = doc.page_content
    metadata = doc.metadata
    
    try:
        # Parse the code into an Abstract Syntax Tree
        tree = ast.parse(code)
        imports = []
        
        for node in tree.body:
            # Group all imports together
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                chunk_code = ast.get_source_segment(code, node)
                if chunk_code:
                    imports.append(chunk_code)
            
            # Extract distinct Functions and Classes as their own perfect chunks
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                chunk_code = ast.get_source_segment(code, node)
                if chunk_code:
                    new_metadata = metadata.copy()
                    new_metadata["node_type"] = type(node).__name__  # Tags it as a Class or Function
                    new_metadata["node_name"] = node.name            # Adds the actual function/class name
                    chunks.append(Document(page_content=chunk_code, metadata=new_metadata))
                    
        # Add the grouped imports as a single dedicated chunk
        if imports:
            import_text = "\n".join(imports)
            import_metadata = metadata.copy()
            import_metadata["node_type"] = "Imports"
            chunks.append(Document(page_content=import_text, metadata=import_metadata))
            
        return chunks
        
    except SyntaxError:
        # If the code is broken and cannot be parsed, return None to trigger the fallback
        return None 

def process_github_repo(repo_url):
    """Clones a repo, applies AST parsing for Python, and chunks other files by Language."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(base_dir, "..", "repo")
    db_path = os.path.join(base_dir, "..", "chroma_db")

    chromadb.api.client.SharedSystemClient.clear_system_cache()
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    subprocess.run(["git", "clone", repo_url, repo_path], check=True)

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

    chunks = []
    for doc in docs:
        file_path = doc.metadata.get("source", "")
        _, ext = os.path.splitext(file_path)
        
        # 1. Advanced AST Chunking for Python Files
        if ext == ".py":
            ast_chunks = extract_python_ast_chunks(doc)
            if ast_chunks: 
                chunks.extend(ast_chunks)
                continue # Skip the fallback logic and move to the next file
                
        # 2. Fallback: LangChain Language Splitters for other languages or broken .py files
        if ext in EXTENSION_MAPPING:
            splitter = RecursiveCharacterTextSplitter.from_language(
                language=EXTENSION_MAPPING[ext],
                chunk_size=1000,
                chunk_overlap=200
            )
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            
        chunks.extend(splitter.split_documents([doc]))

    if not chunks:
        raise ValueError("Files were found, but no text could be extracted.")

    Chroma.from_documents(chunks, embeddings, persist_directory=db_path)

    return len(docs), len(chunks)