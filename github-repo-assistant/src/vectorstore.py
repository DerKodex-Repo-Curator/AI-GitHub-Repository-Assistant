from chunker import chunks
from embeddings import embeddings
from langchain_community.vectorstores import Chroma

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="../chroma_db"
)

db.persist()

print("Vector DB created")