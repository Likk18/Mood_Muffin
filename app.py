# app.py
from flask import Flask
from dotenv import load_dotenv
import os

# Import the Blueprint from routes.py
from routes import main_routes

# Load environment variables from .env file
load_dotenv()

# Check for the necessary API key at startup
if not os.getenv("GEMINI_API_KEY"):
    print("🚨 WARNING: GEMINI_API_KEY environment variable not set.")

app = Flask(__name__)

# A secret key is required for Flask session management
# This allows us to store the Spotify token securely for the user
app.secret_key = os.urandom(24)

# Register the blueprint from routes.py
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
