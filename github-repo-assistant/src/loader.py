import os
import shutil
from langchain_community.document_loaders import GitLoader

def load_github_repo(repo_url):
    repo_path = "./temp_repo"
    
    # 1. Clean up the old repository before cloning a new one
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        
    # 2. Clone the new repository
    loader = GitLoader(repo_path=repo_path, clone_url=repo_url, branch="main")
    
    return loader.load()