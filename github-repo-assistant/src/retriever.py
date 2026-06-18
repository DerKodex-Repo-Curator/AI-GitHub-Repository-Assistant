from langchain_community.vectorstores import Chroma
from embeddings import embeddings 
import os

# Get the absolute path to your chroma_db folder
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "chroma_db")

# Connect to the database
db = Chroma(
    persist_directory=db_path,
    embedding_function=embeddings
)

# Set it up as a retriever to fetch the top 5 most relevant code chunks
retriever = db.as_retriever(search_kwargs={"k": 5})