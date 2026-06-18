import streamlit as st
import uuid
from chain import chain

# 1. Page Configuration (Keep your existing config)
st.set_page_config(
    page_title="GitHub Assistant", 
    page_icon="🧩", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEW: Inject Amazing Custom CSS ---
st.markdown("""
<style>
    /* Hide Streamlit default header, footer, and hamburger menu for a clean app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Global App Background (GitHub Dark theme) */
    .stApp {
        background-color: #0d1117;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d;
    }

    /* Style the Chat Input Container */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Sleek Chat Input Box */
    .stChatInputContainer > div {
        border-radius: 20px !important;
        border: 1px solid #30363d !important;
        background-color: #161b22 !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease;
    }
    
    /* Glow effect when typing */
    .stChatInputContainer > div:focus-within {
        border-color: #58a6ff !important;
        box-shadow: 0 0 15px rgba(88, 166, 255, 0.2) !important;
    }

    /* Style the Chat Messages (Bubbles) */
    .stChatMessage {
        background-color: #161b22;
        border-radius: 12px;
        border: 1px solid #21262d;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    /* Typography Adjustments */
    h1, h2, h3, h4 {
        color: #c9d1d9 !important;
        font-family: 'Inter', sans-serif;
    }
    p, span, div {
        color: #8b949e;
    }

    /* Custom Scrollbar for a premium feel */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0d1117; 
    }
    ::-webkit-scrollbar-thumb {
        background: #30363d; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #58a6ff; 
    }
</style>
""", unsafe_allow_html=True)




# 2. Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Control Panel")
    st.markdown("Manage your assistant session here.")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        # Reset the messages and generate a fresh session ID
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.success("Chat history cleared!")
        
    st.divider()
    
    # Repository Status Dashboard
    st.subheader("📊 System Status")
    st.markdown("**Target Repo:** `pallets/flask`")
    st.markdown("**Status:** ✅ Indexed & Ready")
    st.markdown("**Vector DB:** ChromaDB")
    st.markdown("**LLM Engine:** Llama 3.1 (Groq)")

# 3. Main Interface Header
st.title("🧩 GitHub Repository Assistant")
st.markdown("Your AI pair programmer. Ask complex questions about the codebase, and get answers backed by the actual source code.")
st.divider()

# 4. Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Empty State / Welcome Screen
if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! Try asking one of the questions below to get started.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- *What is the main purpose of the Flask class?*")
        st.markdown("- *How are routes handled in this repository?*")
    with col2:
        st.markdown("- *Can you explain how the Request object is structured?*")
        st.markdown("- *Show me a code example of error handling.*")

# 6. Render Chat History with Custom Avatars
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 7. Chat Input & Processing
if prompt := st.chat_input("Ask a question about the Flask repository..."):
    
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Scanning repository and thinking..."):
            try:
                # Invoke the chain with the session ID for memory
                response = chain.invoke(
                    {"question": prompt},
                    config={"configurable": {"session_id": st.session_state.session_id}}
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")