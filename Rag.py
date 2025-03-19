import openai
import fitz  
import time

OPENAI_API_KEY = FIRST_HALF + SECOND_HALF
FIRST_HALF = "sk-proj-sYZDvt8xRN67yztQ5CuxXWXDll-BxDGa7rHkGWcNhsLLijf9rKk"
SECOND_HALF = "fxDNCnXeEYkmjNEPcStBCzVT3BlbkFJV2suua7LrY58vVkZpnKhozA7bNDnuh3agkJ2OLaEsXxhvjNkEbxQB67wISYgzVVwX7azoa52QA
client = openai.OpenAI(api_key=OPENAI_API_KEY)

file_path = "AI-Powered RAG Model for a Virtual Bank Loan Officer.pdf"  
with fitz.open(file_path) as pdf:
    pdf_text = "\n".join(page.get_text("text") for page in pdf)  

pdf_text = pdf_text[:3000]  

assistant = client.beta.assistants.create(
    name="Loan Assistant",
    instructions="You are a financial assistant. Provide short, crisp, and human-like responses to user queries. Answer only what is asked and avoid unnecessary details. Use the provided document to assist with loan-related questions.",
    model="gpt-4-turbo"
)
assistant_id = assistant.id  
print(f"✅ Created Assistant ID: {assistant_id}")

# Step 3: Create a thread
thread = client.beta.threads.create()
thread_id = thread.id
print(f"✅ Created Thread ID: {thread_id}")

# Step 4: Chat loop
print("\n💬 Chat with the assistant! Type 'exit' to quit.\n")
while True:
    query = input("You: ")
    
    if query.lower() == "exit":
        print("👋 Exiting chat. Have a great day!")
        break

    full_prompt = f"Document:\n{pdf_text}\n\nUser: {query}"

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=full_prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id 
    )

    # Wait for response
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    # Retrieve and print response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response_text = messages.data[0].content[0].text.value

    print("\n🤖 AI:", response_text, "\n")