from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Import your configured LLM and Retriever
from llm import llm
from retriever import retriever

# 1. Define the System Prompt with a Memory Placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert coding assistant analyzing a GitHub repository.\n"
               "Use the following pieces of retrieved context to answer the question.\n"
               "If you don't know the answer, just say that you don't know.\n"
               "Keep your explanations clear and provide code snippets if helpful.\n\n"
               "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"), # This is where past messages go!
    ("human", "{question}")
])

# 2. Helper function to format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 3. Create a temporary memory store for the session
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 4. Build the core RAG Chain
# We use RunnablePassthrough.assign so we can pass the question to the retriever 
# while keeping it intact for the prompt.
rag_chain = (
    RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | format_docs
    )
    | prompt
    | llm
    | StrOutputParser()
)

# 5. Wrap the chain with the Memory Module
chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)