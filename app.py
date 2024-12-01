from flask import Flask

app = Flask(__name__, template_folder='templates')
    
# Import and register routes
from routes import main
app.register_blueprint(main)

if __name__ == "__main__":
    app.run()
