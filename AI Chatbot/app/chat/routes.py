from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify

from functools import wraps
import uuid

from app.chat.logic import handle_send_message
from app.chat.memory import save_conversation, get_all_conversations, delete_conversation, edit_conversation_name

chat = Blueprint('chat', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@chat.route('/chat')
@chat.route('/chat/<conversation_id>')
@login_required
def chat_page(conversation_id=None):
    return render_template('chat/chat.html', conversation_id=conversation_id)

@chat.route('/send_message', methods=['POST'])
@login_required
def send_message():
    user_id = session['user_id']
    conversation_id = request.json.get('conversation_id')
    user_message = request.json.get('message')
    selected_model = request.json.get('model')
    
    ai_response = handle_send_message(user_id, conversation_id, user_message, selected_model)
    
    return jsonify({'response': ai_response})

@chat.route('/get_conversations', methods=['GET'])
@login_required
def get_conversations():
    user_id = session['user_id']
    conversations = get_all_conversations(user_id)

    return jsonify(conversations)

@chat.route('/create_conversation', methods=['POST'])
@login_required
def create_conversation():
    user_id = session['user_id']
    conversation_id = str(uuid.uuid4())

    save_conversation(user_id, conversation_id, [], name=f'Conversation {conversation_id}')

    return jsonify({'conversation_id': conversation_id})

@chat.route('/delete_conversation/<conversation_id>', methods=['DELETE'])
@login_required
def delete_conversation_route(conversation_id):
    user_id = session['user_id']
    delete_conversation(user_id, conversation_id)
    
    return '', 204

@chat.route('/edit_conversation_name/<conversation_id>', methods=['POST'])
@login_required
def edit_conversation_name_route(conversation_id):
    user_id = session['user_id']
    new_name = request.json.get('name')

    edit_conversation_name(user_id, conversation_id, new_name)
    
    return '', 204

@chat.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
