import streamlit as st
import time
import uuid
import os
from dotenv import load_dotenv

# 1. BULLETPROOF ENV LOADER
# This forces Python to look in the 'src' folder for the .env file, 
# completely bypassing any terminal pathing issues.
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# (Note: If you already moved the .env file out to the main github-repo-assistant folder, 
# change the line above to: load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env")) )

from ingest import process_github_repo

# Import your LLM chain
from chain import get_chain


st.set_page_config(page_title="AI GitHub Assistant")

# Initialize session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_initialized" not in st.session_state:
    st.session_state.repo_initialized = False
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.sidebar.title("Repository Settings")
repo_url = st.sidebar.text_input("Enter GitHub URL:", placeholder="https://github.com/user/repo")

if st.sidebar.button("Initialize Repository"):
    if repo_url:
        with st.spinner("Cloning, chunking, and indexing..."):
            try:
                # 1. Run the NEW ingestion engine that safely handles file locks!
                num_docs, num_chunks = process_github_repo(repo_url)
                    
                # 2. Tell the UI it is ready
                st.session_state.repo_initialized = True
                    
                # 3. Clear past chat history so it doesn't mix up the old repo
                st.session_state.messages = []
                st.session_state.session_id = str(uuid.uuid4())
                    
                st.success(f"Repository loaded! Processed {num_docs} files into {num_chunks} chunks.")
                    
                    # Force a quick UI refresh to reconnect to the fresh database
                time.sleep(2)
                st.rerun()
                    
            except Exception as e:
                st.error(f"Error loading repo: {e}")
    

# Chat Interface
st.title("Chat with your Repo")

# Display historical messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.get("repo_initialized", False):
    if prompt := st.chat_input("Ask a question about the repository..."):
        
        # 1. Add user message to UI state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Generate and display the AI's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Execute your LangChain logic with the fresh chain
                    response = get_chain().invoke(
                        {"question": prompt},
                        config={"configurable": {"session_id": st.session_state.session_id}}
                    )

                    
                    st.markdown(response)
                    
                    # Save AI response to UI state
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
else:
    st.info("Please initialize a repository in the sidebar to start chatting.")