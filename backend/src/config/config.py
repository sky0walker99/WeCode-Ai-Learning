import os

# Config of ai models
generation_config = {
    "temperature": 0.22,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"}

#Score Variables initialization
socratic_score = 0
feynman_score = 0
custom_score = 0

#Database 
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'model_sentiment.db')

# def update_score(result, current_score, model_name):
#     review = ["positive", "neutral", "negative"]
#     if result == review[0]:
#         current_score += 1
#         update_positive_sentiment(model_name)  # Update positive sentiment count in DB
#     elif result == review[2]:
#         current_score -= 1
#     return current_score
