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
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_blueprint)
CORS(app)



# Start the server
if __name__ == '__main__':
    app.run(debug=True)


# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])



# Initialize database 
init_db()


# Assinging current chat and current model for main interaction loop.
current_model = socratic_model
current_chat = socratic_model.chat




"""
# Main interaction loop
while True:
    try:
        user_prompt = input("Prompt: ")
        
        # Sentiment analysis result
        result = sentiment_model.get_result_sentiment(user_prompt)
        # Response Generation and saving chat in history.
        ai_response = current_model.get_response(user_prompt)
        save_chat_history("socratic",user_prompt, ai_response) # saving chat history with category.
        print(f"WeCode Ai: {ai_response}")
        
        # Updating score and switching the model
        
        if current_model == socratic_model:
            socratic_score = socratic_model.update_score(result, socratic_score , "socratic")
            if socratic_score < -2:
                current_model = feynman_model
                current_chat = feynman_model.chat
                socratic_score = 0  # Reset score for next model
                print("Switching to Feynman model...")

        elif current_model == feynman_model:
            feynman_score = feynman_model.update_score(result, feynman_score, "feynman")
            if feynman_score < -2:
                current_model = socratic_model
                current_chat = socratic_model.chat
                feynman_score = 0  # Reset score for next model
                print("Switching to custom model...")

    except KeyboardInterrupt:
        break

"""
