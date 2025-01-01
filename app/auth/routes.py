from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .local_db import load_users, save_users
from .smtp_utils import send_email

import uuid
import time

import os
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.getenv('EMAIL')

auth = Blueprint('auth', __name__)

class User:
    def __init__(self, email, password):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = generate_password_hash(password)
        self.reset_token = None

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'reset_token': self.reset_token
        }

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        users = load_users()
        user = next((u for u in users if u['email'] == email), None)

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('chat.chat_page'))
        
        return render_template('auth/login.html', error = 'Invalid credentials or account does not exist')

    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')

        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return render_template('auth/register.html', error = 'Passwords do not match')

        users = load_users()

        if any(u['email'] == email for u in users):
            return render_template('auth/register.html', error = 'Email already registered')

        user = User(email=email, password=password)
        users.append(user.to_dict())

        save_users(users)

        return render_template('auth/register.html', success='Registration successful. Please log in.')

    return render_template('auth/register.html')

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        user_email = request.form.get('email')

        users = load_users()
        user = next((u for u in users if u['email'] == user_email), None)

        if not user:
            return render_template('auth/forgot_password.html', error = 'Email not registered')

        user['reset_token'] = str(uuid.uuid4())
        save_users(users)

        reset_link = url_for('auth.reset_password', token=user['reset_token'], _external=True)
        subject = "Password Reset Request"
        body = f"Click the link to reset your password: {reset_link}"

        msg = MIMEMultipart()
        msg["From"] = ENDPOINT
        msg["To"] = user_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            start_time = time.time()
            send_email(msg)
            end_time = time.time()
        except Exception as e:
            return render_template('auth/forgot_password.html', error=f'An error occurred: {e}')

        return render_template('auth/forgot_password.html', success=f'Password reset instructions sent to your email ({end_time - start_time:.2f}s).')

    return render_template('auth/forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            return render_template('auth/reset_password.html', error = 'Passwords do not match')

        users = load_users()
        user = next((u for u in users if u['reset_token'] == token), None)

        if not user or user['reset_token'] != token:
            return render_template('auth/reset_password.html', error = 'Invalid reset token')

        if check_password_hash(user['password'], new_password):
            return render_template('auth/reset_password.html', error = 'New password cannot be the same as the old password')

        user['password'] = generate_password_hash(new_password)
        user['reset_token'] = None  # Reset token after password reset

        save_users(users)

        return render_template('auth/reset_password.html', success='Password has been reset successfully.')

    return render_template('auth/reset_password.html', token=token)

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))
