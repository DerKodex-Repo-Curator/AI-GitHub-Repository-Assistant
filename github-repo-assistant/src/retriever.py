import os
from langchain_chroma import Chroma
from embeddings import embeddings

def get_retriever():
    """Connects to the vector database and returns a retriever with a massive context window."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "chroma_db")

    # 1. Reconnect to the local Chroma vector store
    db = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )

    # 2. Return the retriever with 'k' set to 15 for deep Code Reviews
    return db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 15}
    )