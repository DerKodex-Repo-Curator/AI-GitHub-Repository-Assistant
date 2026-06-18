from langchain_community.document_loaders import DirectoryLoader, TextLoader
import os

# Create a bulletproof absolute path to the repo folder
base_dir = os.path.dirname(os.path.abspath(__file__))
repo_path = os.path.join(base_dir, "..", "repo")

# Initialize the loader
loader = DirectoryLoader(
    repo_path,
    glob="**/*.py",
    loader_cls=TextLoader,
    show_progress=True
)

# Load the documents into the 'docs' variable
docs = loader.load()
print(f"Loaded {len(docs)} documents from the repo.")