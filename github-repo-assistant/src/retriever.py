from langchain_community.vectorstores import Chroma
from embeddings import embeddings
import os

def get_retriever():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "chroma_db")
    
    # Connect to the database dynamically
    db = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    # Return the retriever
    return db.as_retriever(search_kwargs={"k": 5})