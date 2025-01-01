import json
import os

LOCAL_STORAGE_PATH = 'app/storage/users'
INDENT = 4

def load_users():
    if not os.path.exists(LOCAL_STORAGE_PATH):
        os.makedirs(LOCAL_STORAGE_PATH)

        users = []

        with open(f'{LOCAL_STORAGE_PATH}/users.json', 'w') as file:
            json.dump(users, file, indent=INDENT)
            
    with open(f'{LOCAL_STORAGE_PATH}/users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open(f'{LOCAL_STORAGE_PATH}/users.json', 'w') as file:
        json.dump(users, file, indent = INDENT)
