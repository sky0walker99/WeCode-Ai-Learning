import sqlite3
from dotenv import load_dotenv
import os
import google.generativeai as genai
from IPython.display import Image
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from config import *
from database import *
from models import *
from flask import Flask
from routes import api_blueprint  # Import the blueprint

# Initialization of models
sentiment_model = SentimentModel(model_name= "gemini-1.5-flash", generation_config = generation_config, system_instruction = sentiment_sys_instruct)
socratic_model = SocraticModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = socratic_sys_instruct)
feynman_model = FeynmanModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = feynman_sys_instruct)
custom_model = CustomModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = cusotm_sys_instruct)

# Create web application instance
app = Flask(__name__,static_folder='dist')

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Register the blueprint
app.register_blueprint(api_blueprint)

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])



# Initialize database 
init_db()


# Assinging current chat and current model for main interaction loop.
current_model = socratic_model
current_chat = socratic_model.chat

# Start the server
if __name__ == '__main__':
    app.run(host="0.0.0.0")
    
    
# Creating web application instance
#app = Flask(__name__)



