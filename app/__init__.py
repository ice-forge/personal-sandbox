from flask import Flask

import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

    from .routes import main
    from .auth import init_auth
    from .chat.routes import chat
    
    app.register_blueprint(main)
    init_auth(app)
    app.register_blueprint(chat)

    return app
