from app.chat.memory import save_conversation, get_conversation

import requests

import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

def handle_send_message(user_id, conversation_id, user_message, selected_model):
    data = get_conversation(user_id, conversation_id)
    conversation = data.get('conversation', [])
    conversation.append({"role": "user", "content": [{"type": "text", "text": user_message}]})

    ai_response = send_message_to_model(conversation, selected_model)
    conversation.append({"role": "system", "content": [{"type": "text", "text": ai_response}]})

    save_conversation(user_id, conversation_id, conversation, name=data.get('name'))
    return ai_response

# <-- Add your AI model functions here -->

def send_message_to_openai(conversation):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }

    system_message = {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a helpful AI assistant."
            }
        ]
    }

    messages = [system_message] + conversation

    payload = {
        "messages": messages
    }

    try:
        response = requests.post(AZURE_OPENAI_ENDPOINT, headers = headers, json = payload)
        response.raise_for_status()

        result = response.json()['choices'][0]['message']['content']
        return result
    except requests.exceptions.RequestException as e:
        return f"An error occurred. Please ensure your .env files are properly configured.\n\nException: {e}"

def send_message_to_model(conversation, model):
    model_functions = {
        'ChatGPT 4o': send_message_to_openai,
    }

    return f"Assistant: {model}\n\n" + model_functions.get(model, lambda _: f"Unsupported model: {model}")(conversation)
