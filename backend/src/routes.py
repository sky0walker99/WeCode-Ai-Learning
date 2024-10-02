# routes.py
from flask import Flask , Blueprint, request, jsonify
from models import *
from abc import ABC, abstractmethod
from config import *
from dotenv import load_dotenv
import sqlite3
import os
import google.generativeai as genai
from IPython.display import Image
import requests
from flask_cors import CORS
from datetime import datetime, timedelta
from config import *
from database import *


# Create web application instance
app = Flask(__name__)

# Score function to evaluate sentiment and update score
def update_score(result, current_score, model_name):
    review = ["positive", "neutral", "negative"]
    if result == review[0]:
        current_score += 1
        update_positive_sentiment(model_name)  # Update positive sentiment count in DB
    elif result == review[2]:
        current_score -= 1
    return current_score

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Creating web application instance
api_blueprint = Blueprint('api', __name__)

#Score Variables initialization
socratic_score = 0
feynman_score = 0
custom_score = 0

    
# Initialization of models
sentiment_model = SentimentModel(model_name= "gemini-1.5-flash", generation_config = generation_config, system_instruction = sentiment_sys_instruct)
socratic_model = SocraticModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = socratic_sys_instruct)
feynman_model = FeynmanModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = feynman_sys_instruct)
custom_model = CustomModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = cusotm_sys_instruct)

# The endpoint should be set up to handle POST requests since the user's input will be sent as a JSON payload
@api_blueprint.route('/api/get_user_input', methods=['POST'])
def get_user_input():
    global socratic_score
    global feynman_score
    global custom_score

    
    # Assinging current chat and current model for main interaction loop.
    current_model = socratic_model
    current_chat = socratic_model.chat

    data = request.get_json()                  # Extract JSON data from the request
    user_prompt = data.get('user_input', '')   # Get the user input from the JSON data

    # Ensure that sentiment_model and current_model are defined globally or imported
    result = sentiment_model.get_result_sentiment(user_prompt)
    
    # Response generation and saving chat in history
    ai_response = current_model.get_response(user_prompt)
    # save_chat_history("socratic", user_prompt, ai_response)
    
    print(f"WeCode Ai: {ai_response}")
    
    if current_model == socratic_model:
        socratic_score = socratic_model.update_score(result, socratic_score , "socratic")
        print(f"socratic score: {socratic_score} ")
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

    # Process the input, pass it to an AI model, and return the response
    response_data = {
        'received_input': user_prompt,
        'status': 'success',
        'ai_response': ai_response
    }
    return jsonify(response_data), 200


@api_blueprint.route('/api/submit_input', methods =['PSOT'])   # The route for giving the input from user to ai models.
def submit_input_to_ai():
    data = request.get_json()
    user_input = data.get('user_input', '') 
    ai_result = f"ai: {user_input}"
    response_data = {
        'received_input': user_input,
        'ai_result': ai_result,
        'status': 'success'
    }
    return jsonify(response_data), 200


@api_blueprint.route("/api/chat_history", methods=["GET"])
def get_chat_history():
    # Extract the category from the query parameters, defaulting to 'today' if not provided
    category = request.args.get("category", "today")

    # Retrieve chat history based on the requested category
    chat_history = get_chat_by_category(category)

    # If there's no history found, return an appropriate message
    if not chat_history:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"No chats found for category: {category}",
                }
            ),
            404,
        )

    # Format the retrieved history into a list of dictionaries for JSON response
    chat_data = []
    for chat in chat_history:
        chat_data.append(
            {
                "model": chat[0],
                "user_message": chat[1],
                "ai_response": chat[2],
                "timestamp": chat[3],
            }
        )

    # Return the chat history in JSON format
    return jsonify({"status": "success", "chat_history": chat_data}), 200


# Start the server
if __name__ == '__main__':
    app.run(debug=True)