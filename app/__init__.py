from flask import Flask

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Register Blueprints
    from .routes import main  # Import your Blueprint
    app.register_blueprint(main)

    # Additional Configurations (if any)
    app.config['SECRET_KEY'] = 'your_secret_key_here'  # Example: Add a secret key

    return app
