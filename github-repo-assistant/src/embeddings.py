from langchain_huggingface import HuggingFaceEmbeddings

# Initialize a fast, free local model that is excellent for reading code and text
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")