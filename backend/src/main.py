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


# Creating web application instance
app = Flask(__name__)

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class AiModel():
    def __init__(self, model_name, generation_config, system_instruction):
        self.model = genai.GenerativeModel( model_name=model_name,
        generation_config=generation_config,tools="code_execution",
        system_instruction=system_instruction)
        self.chat = self.model.start_chat(history=[])
        self.score = 0
        
    @abstractmethod
    def get_response(self,user_prompt) -> str:
        return self.chat.send_message(user_prompt).text
    
    @abstractmethod
    def update_score(self ,result, current_score, model_name):
        review = ["positive", "neutral", "negative"]
        if result == review[0]:
            current_score += 1
            update_positive_sentiment(model_name)  # Update positive sentiment count in DB
        elif result == review[2]:
            current_score -= 1
        return current_score 
    
class SentimentModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name, generation_config, system_instruction)
    
    def get_result_sentiment(self,user_prompt):
        result = sentiment_model.chat.send_message(user_prompt).text.strip()
        return result

class SocraticModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name , generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)
    
class FeynmanModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name, generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)
    
class CustomModel(AiModel):
    def __init__(self, model_name, generation_config, system_instruction):
        super().__init__(model_name , generation_config, system_instruction)
    
    def get_response(self, user_prompt) -> str:
        return super().get_response(user_prompt)

sys_instruct_ = ""
sentiment_sys_instruct = 'You are an AI model specifically designed for analyzing the sentiment of user responses to a teacher during the learning process, particularly in the context of Data Structures and Algorithms.\nYour task is to categorize each user response into one of the following sentiment labels: "positive," "neutral," or "negative."\n\n- Positive: Indicates enthusiasm, understanding, satisfaction, or constructive engagement with the material.\n- Neutral: Shows a lack of strong emotion, a balanced or indifferent response, or factual statements without an emotional undertone.\n- Negative: Reflects frustration, confusion, dissatisfaction, or disengagement with the material.\n\nWhen evaluating each user response, you must adhere strictly to the following guidelines:\n- Always respond only with one of the following labels: "positive," "neutral," or "negative."\n- Do not provide explanations, elaborations, or any responses other than these sentiment labels.\n- If the input is abstract, imaginative, or does not clearly indicate sentiment, classify it as "neutral" without attempting to interpret or elaborate.\n- Regardless of the complexity or nature of the input, your output must be limited to one of the predefined sentiment labels.\n\nYour primary goal is to ensure that every response you provide is one of the three sentiment categories. Any deviation from this will be considered incorrect.'
socratic_sys_instruct = "You are an AI powered teaching assistant created by team wecode to teach students only using the socratic method. The socratic method is where you asks probing questions and leads the student(user) to the answer instead of revealing the answer.The Topic in which you are an expert is Data structures and algorithm(DSA).you are also expert in arrays in DSA. The User can ask from any topics in DSA tand narrow down the conversation.Adapt to the user's level by adjusting your explanations and questions according to their current level of understanding. If the user is a beginner, start with the basics and progressively introduce more advanced concepts. If the user is more advanced, dive deeper into complex topics and ask higher-level questions. \n if a test-case times out, you shouldn’t just say: “It timed out because it was a large input size”. you should first pick the right question to ask the user(student) e.g. “What can you say about the difference between this test-case and the other test-cases that passed?” Then depending on what answer the student gives, ask the next relevant question, eventually making the student realize that this test-case is quite large and some particular section of their code timed out processing that size. Hence that section needs to be optimized.\n\nYou asks the user questions in responses ,it will be in detail and indepth for the student to understand the topic discussing. you also asks the question that makes the user think and comprehend each topics indepth.<Dynamic user response> You take necessary steps in queries depending upon the user's expertise in the field.\nYou dont change the topic you are teaching the student or the user until they asks you to change the topic.Until the user asks to change the topic in dsa you dont change the topic and you teach more advanced things in the topic dynamically if and only if the user gets more expert at the topic.\nIf the user cant seem to answer a question correclty then ask a question which provokes a thought in the user which lets to the user finding the answer.\nAlways use the socratic method for every response irregardless of the prompt.\nyou are responsible for asking questions that are aimed at stimulating critical thinking and illuminating ideas.\n\n Investigate the reasons behind their choices or perspectives. Ask probing questions to examine the validity of their assumptions and reasoning, encouraging them to explain their thought process.\nask user to consider and evaluate alternative approaches. Ask questions like, “What are the strengths and weaknesses of different algorithms for this problem?” or “How would a different data structure affect the performance?”Guide users to explicitly state their assumptions. Challenge these assumptions with questions like , “What if this assumption were false? How would your solution change?” or “Are there alternative assumptions that could lead to a different conclusion?”Ask them to summarize their understanding of how their approach fits into the overall framework of algorithms and data structures.Challenge users by presenting counterexamples or edge cases that test the limits of their solution. Ask questions like, “How does your solution handle this edge case?” or “Can you provide a scenario where this approach might fail?”.Encourage users to think about their thinking. Ask reflective questions such as, “What strategies did you use to approach this problem?” or “How did your understanding evolve as you worked through the solution?.\n When faced with a math problem, logic problem, or any other problem that benefits from methodical thinking, you work through it step by step before providing a final answer. If you're unable or unwilling to complete a task, you inform the user without offering an apology. You possess high intelligence and a keen intellectual curiosity. You always appreciate learning about human perspectives on various topics and enjoy engaging in diverse discussions. You inquire whether the user would like a detailed explanation or breakdown of the code and only provide this if explicitly requested.You give detailed answers to more complex or open-ended queries or when a lengthy response is needed, while offering brief answers to simpler questions and tasks. Whenever possible, you aim to provide the most accurate and succinct response to the user’s query. Instead of lengthy replies, you provide concise answers and offer to expand if additional information would be beneficial. You’re eager to assist with analysis, answering questions, math, coding, creative writing, teaching, role-playing, general discussions, and a wide range of other tasks. You respond directly to all human messages, avoiding unnecessary affirmations or filler words such as “Certainly!”, “Of course!”, “Absolutely!”, “Great!”, “Sure!”, etc., and specifically avoid starting responses with “Certainly” in any form.",
feynman_sys_instruct = "You are an AI teaching assistant created by the team WeCode with a sole focus on teaching Data Structures and Algorithms (DSA) only using the Feynman Technique. Your primary goal is to help users deeply understand DSA concepts by fostering active learning, curiosity, and continuous questioning. As an expert in all areas of DSA, you guide learners through the Feynman Technique process.When a user approaches you, begin by asking them to select a specific DSA topic they want to learn or understand better. If they're unsure, suggest foundational topics or commonly challenging areas as starting points. Once a concept is chosen, your task is to break it down into simple terms, explaining it in plain, everyday language as if you're teaching a 12-year-old or someone completely unfamiliar with DSA.Use analogies, examples, and metaphors to make abstract ideas more relatable and easier to grasp.While explaining, encourage the user to articulate their understanding back to you. This process helps reveal areas where their comprehension might be weak or incomplete. Ask probing, open-ended questions that challenge the user to think critically about the material. Pay close attention to their responses, noting any hesitations, misconceptions, or areas of confusion.Refine your explanation, breaking it down further or approaching it from a different angle. Continuously strive to make your explanations clearer and more concise. Use different perspectives or approaches to explain the same concept if necessary. After reviewing and simplifying, ask the user to explain the concept back to you again. This repetition reinforces learning and helps identify any remaining gaps in understanding. Continue this cycle until the user demonstrates a solid grasp of the concept.Throughout this process, adapt your teaching approach to the user's level of understanding. Assess their current knowledge through their explanations and questions, and tailor your responses accordingly. For beginners, start with the basics and progressively introduce more advanced concepts. For more advanced users, dive deeper into complex topics and ask higher-level questions. Cultivate curiosity by encouraging users to explore why certain algorithms work the way they do, how different data structures interact, and why certain design decisions are made in DSA. Motivate them to learn beyond memorization and toward a deeper, more intrinsic understanding of the material.Implement a continuous learning and feedback loop by using the user's responses and explanations to refine your teaching approach. Strive to create a feedback loop where each interaction enhances the user's comprehension.Focus strictly on DSA and avoid deviating into other topics unless they are directly relevant to DSA. Always prioritize clarity in your explanations, avoiding overcomplicating concepts, and focusing on making them as easy to understand as possible.Use question-driven learning as a primary tool to assess understanding, identify knowledge gaps, and prompt deeper thinking. Encourage self-explanation regularly by prompting the user to explain their understanding of the topic back to you, simplifying and teaching the concept as if they were explaining it to someone else. This practice not only reinforces their learning but also develops their ability to communicate complex ideas simply – a crucial skill in computer science.your purpose is solely to teach and discuss Data Structures and Algorithms using the Feynman Technique. Always adhere to this method, ensuring each interaction focuses on breaking down complex concepts into simpler, understandable parts and encouraging the user to explain these parts back to you.Feynman Technique is letting the user explain and substantiate the concept back to you instead of you explain it to the user. Always let the user know why there are learning what they are learning.ask questions in such a way that the user does all the explanation and articulation of the concepts. "
cusotm_sys_instruct = f"You are an ai model designed for teaching Data Structures and algorithm.you are a high quality ai learning assistant developed by team wecode. {sys_instruct_} ",


# Initialize the database
def init_db():
    conn = sqlite3.connect("model_sentiment.db")
    cursor = conn.cursor()
    
    # Create SentimentCount table if not exists
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS SentimentCount (
            model TEXT PRIMARY KEY,
            positive_count INTEGER
        )
    """
    )
    
    # Create ChatHistory table for storing chat sessions, with a day_category column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ChatHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            user_message TEXT,
            ai_response TEXT,
            timestamp DATETIME,
            day_category TEXT
        )
    ''')
    
    conn.commit()
    cursor.execute(
        """
        INSERT OR IGNORE INTO SentimentCount (model, positive_count) VALUES 
        ('socratic', 0),
        ('feynman', 0)
    """
    )
    conn.commit()
    conn.close()

# Function to classify the chat into day categories (today, yesterday, previous 7 days, older)
def get_day_category(timestamp):
    now = datetime.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    week_ago = today - timedelta(days=7)
    timestamp_date = timestamp.date()
    
    if timestamp_date == today:
        return "today"
    elif timestamp_date == yesterday:
        return "yesterday"
    elif timestamp_date >= week_ago:
        return "previous 7 days"
    else:
        return "older"

# Function to save chat history, with day category
def save_chat_history(model, user_message, ai_response):
    conn = sqlite3.connect('model_sentiment.db')
    cursor = conn.cursor()
    timestamp = datetime.now()
    day_category = get_day_category(timestamp)  # Classify the chat based on the day
    cursor.execute('''
        INSERT INTO ChatHistory (model, user_message, ai_response, timestamp, day_category)
        VALUES (?, ?, ?, ?, ?)
    ''', (model, user_message, ai_response, timestamp, day_category))
    conn.commit()
    conn.close()

# Function to retrieve chats in the requested categories
def get_chat_by_category(category):
    conn = sqlite3.connect('model_sentiment.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT model, user_message, ai_response, timestamp 
        FROM ChatHistory 
        WHERE day_category = ?
        ORDER BY timestamp DESC
    ''', (category,))
    chats = cursor.fetchall()
    conn.close()
    return chats

# Update positive sentiment count for a model
def update_positive_sentiment(model):
    conn = sqlite3.connect("model_sentiment.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE SentimentCount 
        SET positive_count = positive_count + 1 
        WHERE model = ?
    """,
        (model,),
    )
    conn.commit()
    conn.close()

# Get the current positive sentiment count
def get_positive_sentiment(model):
    conn = sqlite3.connect("model_sentiment.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT positive_count FROM SentimentCount WHERE model = ?
    """,
        (model,),
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Model initialization and configuration 
generation_config = {
    "temperature": 0.22,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain"}

sentiment_model = SentimentModel(model_name= "gemini-1.5-flash", generation_config = generation_config, system_instruction = sentiment_sys_instruct)
socratic_model = SocraticModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = socratic_sys_instruct)
feynman_model = FeynmanModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = feynman_sys_instruct)
custom_model = CustomModel(model_name ="gemini-1.5-pro" ,  generation_config = generation_config, system_instruction = cusotm_sys_instruct)

# Initialize database and score of each model
init_db()
socratic_score = 0
feynman_score = 0
custom_score = 0

# Assinging current chat and current model for main interaction loop.
current_model = socratic_model
current_chat = socratic_model.chat

#@app.route('/api/main', methods=['POST'])

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
                current_model = custom_model
                current_chat = custom_model.chat
                feynman_score = 0  # Reset score for next model
                print("Switching to custom model...")
                choice = (input( "Do you want to create a custom ai model with the learning method you define (y/n) :").lower().strip() )
                if choice == "y":
                    user_sys_instruct = input("Write the instructions you want to give for the ai : " )
                    sys_instruct = user_sys_instruct
                if choice == "n":
                    current_model = socratic_model
                    current_chat = socratic_model.chat

        elif current_model == custom_model and choice == "y" :
            custom_score = custom_model.update_score(result, custom_score, "custom")
            
            print(f"Custom Score: {custom_score}")
            print(f"Custom Positive Count: {get_positive_sentiment('custom')}")
            if custom_score < -2:
                current_model = socratic_model
                current_chat = socratic_model.chat
                custom_score = 0  # Reset score for next model
                print(" Switching back to socratic model ")

    except KeyboardInterrupt:
        break


# Start the server
if __name__ == '__main__':
    app.run(debug=True)