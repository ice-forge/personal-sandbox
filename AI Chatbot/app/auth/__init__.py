import pydocumentdb.document_client as document_client
import os

from .routes import auth

def init_auth(app):
    # Set Cosmos DB configurations
    app.config['COSMOS_DB_URI'] = os.getenv('COSMOS_DB_URI')
    app.config['COSMOS_DB_KEY'] = os.getenv('COSMOS_DB_KEY')
    app.config['COSMOS_DB_DATABASE'] = os.getenv('COSMOS_DB_DATABASE')
    app.config['COSMOS_DB_CONTAINER'] = os.getenv('COSMOS_DB_CONTAINER')

    # Initialize Cosmos DB client
    app.cosmos_client = document_client.DocumentClient(app.config['COSMOS_DB_URI'], {'masterKey': app.config['COSMOS_DB_KEY']})
    app.cosmos_database = app.config['COSMOS_DB_DATABASE']
    app.cosmos_container = app.config['COSMOS_DB_CONTAINER']

    # Register the blueprint
    app.register_blueprint(auth, url_prefix='/auth')
