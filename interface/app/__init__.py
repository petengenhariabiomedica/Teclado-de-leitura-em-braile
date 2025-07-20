from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
    app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key')

    from .routes import bp
    app.register_blueprint(bp)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    return app

