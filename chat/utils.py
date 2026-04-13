import os

from langchain_openai import ChatOpenAI
from .models import Chats
from django.shortcuts import get_object_or_404

title_model = ChatOpenAI(
    model="nvidia/nemotron-3-super-120b-a12b:free",
    api_key=os.getenv("OpenRouter_key"),
    base_url="https://openrouter.ai/api/v1",
    streaming=False,
    temperature=0.4,
)

def generate_title(user_message,chat_id,user_email):
    messages = [
        ("system", system_prompt),
        ("human", user_message),
    ]
    print("Generating title for message:", user_message)
    response = title_model.invoke(messages).content.strip()
    print("Generated title:", response)
    Chats.objects.filter(
        id=chat_id,
        user_email=user_email
    ).update(title=response)

    return response if response else "New Chat"

models_list=["google/gemma-4-31b-it:free","google/gemma-4-26b-a4b-it:free","nvidia/nemotron-3-super-120b-a12b:free"]

system_prompt ="""
Generate a short chat title (max 5 words).

Focus ONLY on the main intent.
Make it sound like a real app title.

Do NOT:
- repeat the input
- include unnecessary details
- write a sentence

HOW to get the correct title:
Step 1: Identify the main intent of the message.
Step 2: Generate a short title (max 5 words) based on that intent.

Return ONLY the title.
                """
