# services/llm_service.py
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Memory to retain chat history
conversation_memory = []

def chat_with_memory(user_message: str, rag_context: str = ""):
    # Initial system instruction for tone and behavior
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and professional assistant. Use the provided context when available. "
                "Keep your answers short, direct, and avoid unnecessary elaboration. "
                "Be clear and polite. End every response with: 'Do you need more info?'"
            )
        }
    ]

    # Inject RAG context into memory if available
    if rag_context:
        messages.append({
            "role": "system",
            "content": f"The following context may be useful for the conversation:\n{rag_context}"
        })

    # Include chat history
    messages.extend(conversation_memory)

    # Add the current user query
    messages.append({"role": "user", "content": user_message})

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    reply = response.choices[0].message.content.strip()

    # Ensure the response ends properly
    if "do you need more info?" not in reply.lower():
        reply = reply.rstrip(".") + ". Do you need more info?"

    # Save conversation memory
    conversation_memory.append({"role": "user", "content": user_message})
    conversation_memory.append({"role": "assistant", "content": reply})

    return reply

def reset_conversation():
    conversation_memory.clear()
