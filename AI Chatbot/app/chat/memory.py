import json
import os

# Path to the local folder for storing conversations

LOCAL_STORAGE_PATH = os.path.join(os.path.dirname(__file__), '../storage/conversations')
INDENT = 4

if not os.path.exists(LOCAL_STORAGE_PATH):
    os.makedirs(LOCAL_STORAGE_PATH)

def read_conversation_file(path):
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)

        return data
    
    return {'name': None, 'conversation': []}

def write_conversation_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent = INDENT)

def save_conversation(user_id, conversation_id, conversation, name=None):
    user_folder = os.path.join(LOCAL_STORAGE_PATH, user_id)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    conversation_file = os.path.join(user_folder, f'{conversation_id}.json')

    # Try loading existing data to preserve the name if not provided

    old_data = read_conversation_file(conversation_file)

    if name is None and 'name' in old_data:
        name = old_data['name']

    data = {
        'name': name or old_data.get('name'),
        'conversation': conversation
    }

    write_conversation_file(conversation_file, data)

def get_conversation(user_id, conversation_id):
    conversation_file = os.path.join(LOCAL_STORAGE_PATH, user_id, f'{conversation_id}.json')
    return read_conversation_file(conversation_file)

def get_all_conversations(user_id):
    user_folder = os.path.join(LOCAL_STORAGE_PATH, user_id)
    conversations = {}

    if os.path.exists(user_folder):
        for filename in os.listdir(user_folder):
            if filename.endswith('.json'):
                conversation_id = filename[:-5]

                with open(os.path.join(user_folder, filename), 'r') as f:
                    data = json.load(f)
                    conversations[conversation_id] = data

    return conversations

def delete_conversation(user_id, conversation_id):
    conversation_file = os.path.join(LOCAL_STORAGE_PATH, user_id, f'{conversation_id}.json')

    if os.path.exists(conversation_file):
        os.remove(conversation_file)

def edit_conversation_name(user_id, conversation_id, new_name):
    conversation_file = os.path.join(LOCAL_STORAGE_PATH, user_id, f'{conversation_id}.json')

    data = read_conversation_file(conversation_file)
    data['name'] = new_name

    write_conversation_file(conversation_file, data)

def get_all_saved_chats():
    all_chats = []

    for user_folder in os.listdir(LOCAL_STORAGE_PATH):
        user_path = os.path.join(LOCAL_STORAGE_PATH, user_folder)
        
        if os.path.isdir(user_path):
            for filename in os.listdir(user_path):
                if filename.endswith('.json'):
                    with open(os.path.join(user_path, filename), 'r') as f:
                        all_chats.append(json.load(f))
                        
    return all_chats
