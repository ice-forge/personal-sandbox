import json

import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_STORAGE_PATH = 'app/storage/users'
INDENT = 4

def load_users():
    if not os.path.exists(f'{LOCAL_STORAGE_PATH}/users.json'):
        return []
    with open(f'{LOCAL_STORAGE_PATH}/users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open(f'{LOCAL_STORAGE_PATH}/users.json', 'w') as file:
        json.dump(users, file, indent = INDENT)
