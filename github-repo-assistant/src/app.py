from chain import chain
import uuid

print("🤖 Welcome to your GitHub Repository Assistant!")
print("Ask a question about the repository (or type 'exit' to quit).\n")

# Create a unique session ID for this specific chat loop
session_id = str(uuid.uuid4())

while True:
    question = input("You: ")
    
    if question.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break
        
    print("\nThinking...")
    
    try:
        # Pass the question AND the session configuration to the chain
        response = chain.invoke(
            {"question": question},
            config={"configurable": {"session_id": session_id}}
        )
        
        print("\n🤖 Assistant:")
        print(response)
        print("-" * 50 + "\n")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")