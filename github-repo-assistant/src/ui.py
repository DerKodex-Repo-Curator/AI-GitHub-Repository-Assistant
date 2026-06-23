import streamlit as st
import time
import uuid
import os
from dotenv import load_dotenv

# 1. BULLETPROOF ENV LOADER
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

from ingest import process_github_repo
from chain import get_chain

# --- PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="⚡",
    layout="wide", # Uses the full width of the monitor
    initial_sidebar_state="expanded"
)

# --- CUSTOM ENTERPRISE CSS ---
st.markdown("""
    <style>
    /* GitHub Dark Mode Palette */
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    
    /* Sleek Input Fields */
    .stTextInput input { background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 6px; }
    
    /* Premium Button Animations */
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; transition: 0.2s ease-in-out; }
    .stButton>button[kind="primary"] { background-color: #238636; color: white; border: 1px solid rgba(240, 246, 252, 0.1); }
    .stButton>button[kind="primary"]:hover { background-color: #2ea043; border-color: #8b949e; transform: scale(1.02); }
    
    /* Chat Bubble Aesthetics */
    .stChatMessage { background-color: #1c2128; border-radius: 10px; border: 1px solid #30363d; padding: 15px; }
    
    /* Highlighted Metrics */
    [data-testid="stMetricValue"] { color: #58a6ff; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_initialized" not in st.session_state:
    st.session_state.repo_initialized = False
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "trigger_review" not in st.session_state:
    st.session_state.trigger_review = False
if "latest_report" not in st.session_state:
    st.session_state.latest_report = None
if "repo_stats" not in st.session_state:
    st.session_state.repo_stats = {"docs": 0, "chunks": 0}

# --- SIDEBAR: DASHBOARD & CONTROLS ---
with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("Workspace Settings")
    
    repo_url = st.text_input("Target Repository:", placeholder="https://github.com/user/repo")
    
    if st.button("🚀 Initialize Workspace", use_container_width=True):
        if repo_url:
            with st.status("Building Vector Workspace...", expanded=True) as status:
                try:
                    st.write("Cloning repository...")
                    num_docs, num_chunks = process_github_repo(repo_url)
                    
                    st.write("Parsing Abstract Syntax Trees...")
                    st.session_state.repo_stats = {"docs": num_docs, "chunks": num_chunks}
                    
                    st.session_state.repo_initialized = True
                    st.session_state.messages = []
                    st.session_state.latest_report = None
                    st.session_state.session_id = str(uuid.uuid4())
                    
                    status.update(label="Workspace Ready!", state="complete", expanded=False)
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    status.update(label="Build Failed", state="error", expanded=True)
                    st.error(e)

    # Dynamic Metrics Display
    if st.session_state.repo_initialized:
        st.markdown("---")
        st.subheader("📊 Database Stats")
        col1, col2 = st.columns(2)
        col1.metric("Files Parsed", st.session_state.repo_stats["docs"])
        col2.metric("AST Chunks", st.session_state.repo_stats["chunks"])

    # DevSecOps Reviewer Tools
    st.markdown("---")
    st.subheader("🛡️ AI DevSecOps Tools")
    
    if st.button("🔍 Run Full Security Audit"):
        if not st.session_state.get("repo_initialized"):
            st.error("Initialize a workspace first!")
        else:
            st.session_state.trigger_review = True
            st.rerun()

    if st.session_state.get("latest_report"):
        st.download_button(
            label="📥 Download Audit Report",
            data=st.session_state.latest_report,
            file_name="Security_Audit_Report.md",
            mime="text/markdown",
            type="primary",
            use_container_width=True
        )

# --- MAIN CHAT INTERFACE ---
if not st.session_state.get("repo_initialized"):
    # The "Empty State" Hero Screen
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #c9d1d9;'>⚡ AI Repository Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #8b949e;'>Paste a GitHub URL in the sidebar to begin code analysis.</h4>", unsafe_allow_html=True)
else:
    st.title("💬 Codebase Chat")
    
    # Render chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input handlers
    user_prompt = st.chat_input("Ask a question about the architecture, logic, or functions...")
    button_triggered = st.session_state.get("trigger_review", False)
    
    if user_prompt or button_triggered:
        if button_triggered:
            prompt = """Act as a Senior DevSecOps Engineer. Review the codebase context provided for the following:
- 🐛 Bugs and Logic Errors
- 🔒 Security Vulnerabilities
- 🤢 Code Smells (bad practices, anti-patterns)
- ⚡ Performance Bottlenecks

Analyze the code deeply. Generate a structured report formatted EXACTLY with these markdown headings. Do not include introductory text, start directly with the headings:

### 🚨 Critical Issues
### 🔴 High Priority
### 🟡 Medium Priority
### 💡 Suggestions

If no issues are found for a specific category, explicitly state "No issues detected." under that heading."""
            display_message = "🔍 *Running deep AST-level Security & Bug Review...*"
            st.session_state.trigger_review = False 
        else:
            prompt = user_prompt
            display_message = user_prompt
            
        st.session_state.messages.append({"role": "user", "content": display_message})
        with st.chat_message("user"):
            st.markdown(display_message)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing neural context..."):
                try:
                    response = get_chain().invoke(
                        {"question": prompt},
                        config={"configurable": {"session_id": st.session_state.session_id}}
                    )

                    ai_reply = response.get("answer", response) if isinstance(response, dict) else response
                    st.markdown(ai_reply)
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                    
                    if button_triggered:
                        st.session_state.latest_report = ai_reply
                        st.rerun() 
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")