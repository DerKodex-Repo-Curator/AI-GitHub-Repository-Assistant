from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Inside src/llm.py
llm = ChatGroq(
    model_name="llama-3.1-8b-instant", # Updated model name!
    temperature=0.2
)