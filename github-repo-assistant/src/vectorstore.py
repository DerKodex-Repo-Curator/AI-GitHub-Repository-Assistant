import os
import shutil
from langchain_community.vectorstores import Chroma
from embeddings import embeddings 

def create_embeddings(text_chunks):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "..", "chroma_db")
    
    # 1. THE CRUCIAL FIX: Completely delete the old database folder
    if os.path.exists(db_path):
        shutil.rmtree(db_path)
    
    # 2. Create a fresh, uncontaminated database for the new repo
    vectorstore = Chroma.from_documents(
        documents=text_chunks, 
        embedding=embeddings, 
        persist_directory=db_path
    )
    return vectorstore