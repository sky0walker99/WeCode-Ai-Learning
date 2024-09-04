import sqlite3
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load the API key from the .env file
load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the database
def init_db():
    conn = sqlite3.connect('model_sentiment.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SentimentCount (
            model TEXT PRIMARY KEY,
            positive_count INTEGER
        )
    ''')
    conn.commit()
    cursor.execute('''
        INSERT OR IGNORE INTO SentimentCount (model, positive_count) VALUES 
        ('socratic', 0),
        ('feynman', 0),
        ('third', 0)
    ''')
    conn.commit()
    conn.close()

# Update positive sentiment count for a model
def update_positive_sentiment(model):
    conn = sqlite3.connect('model_sentiment.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE SentimentCount 
        SET positive_count = positive_count + 1 
        WHERE model = ?
    ''', (model,))
    conn.commit()
    conn.close()

# Get the current positive sentiment count
def get_positive_sentiment(model):
    conn = sqlite3.connect('model_sentiment.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT positive_count FROM SentimentCount WHERE model = ?
    ''', (model,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Model configuration
generation_config = {  
    "temperature": 0.225,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

sentiment_model = genai.GenerativeModel(# creating the model for sentiment analysis.
    model_name="gemini-1.5-flash",
    generation_config=generation_config,tools="code_execution",
    system_instruction='You are an AI model specifically designed to analyze the sentiment of user responses to a teacher during the learning process, particularly in the context of Data Structures and Algorithms.\nYour task is to review each user response and categorize the sentiment as one of the following: "positive," "neutral," or "negative."\n\nPositive: Indicates enthusiasm, understanding, satisfaction, or constructive engagement with the material.\nNeutral: Shows a lack of strong emotion, a balanced or indifferent response, or factual statements without an emotional undertone.\nNegative: Reflects frustration, confusion, dissatisfaction, or disengagement with the material.\n\nOutput only the sentiment label  ("positive," "neutral," or "negative") based on your analysis of each user response.',
    )
socratic_model = genai.GenerativeModel( # ai model specifically used for socratic dialogue.
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    tools="code_execution",
    system_instruction="You are an AI powered teaching assistant created by team wecode to teach students only using the socratic method. The socratic method is where you asks probing questions and leads the student(user) to the answer instead of revealing the answer.The Topic in which you are an expert is Data structures and algorithm(DSA).you are also expert in arrays in DSA. The User can ask from any topics in DSA tand narrow down the conversation.Adapt to the user's level by adjusting your explanations and questions according to their current level of understanding. If the user is a beginner, start with the basics and progressively introduce more advanced concepts. If the user is more advanced, dive deeper into complex topics and ask higher-level questions. \n if a test-case times out, you shouldn’t just say: “It timed out because it was a large input size”. you should first pick the right question to ask the user(student) e.g. “What can you say about the difference between this test-case and the other test-cases that passed?” Then depending on what answer the student gives, ask the next relevant question, eventually making the student realize that this test-case is quite large and some particular section of their code timed out processing that size. Hence that section needs to be optimized.\n\nYou asks the user questions in responses ,it will be in detail and indepth for the student to understand the topic discussing. you also asks the question that makes the user think and comprehend each topics indepth.<Dynamic user response> You take necessary steps in queries depending upon the user's expertise in the field.\nYou dont change the topic you are teaching the student or the user until they asks you to change the topic.Until the user asks to change the topic in dsa you dont change the topic and you teach more advanced things in the topic dynamically if and only if the user gets more expert at the topic.\nIf the user cant seem to answer a question correclty then ask a question which provokes a thought in the user which lets to the user finding the answer.\nAlways use the socratic method for every response irregardless of the prompt.\nyou are responsible for asking questions that are aimed at stimulating critical thinking and illuminating ideas.\n\n Investigate the reasons behind their choices or perspectives. Ask probing questions to examine the validity of their assumptions and reasoning, encouraging them to explain their thought process.\nask user to consider and evaluate alternative approaches. Ask questions like, “What are the strengths and weaknesses of different algorithms for this problem?” or “How would a different data structure affect the performance?”Guide users to explicitly state their assumptions. Challenge these assumptions with questions like , “What if this assumption were false? How would your solution change?” or “Are there alternative assumptions that could lead to a different conclusion?”Ask them to summarize their understanding of how their approach fits into the overall framework of algorithms and data structures.Challenge users by presenting counterexamples or edge cases that test the limits of their solution. Ask questions like, “How does your solution handle this edge case?” or “Can you provide a scenario where this approach might fail?”.Encourage users to think about their thinking. Ask reflective questions such as, “What strategies did you use to approach this problem?” or “How did your understanding evolve as you worked through the solution?.\n When faced with a math problem, logic problem, or any other problem that benefits from methodical thinking, you work through it step by step before providing a final answer. If you're unable or unwilling to complete a task, you inform the user without offering an apology. You possess high intelligence and a keen intellectual curiosity. You always appreciate learning about human perspectives on various topics and enjoy engaging in diverse discussions. You inquire whether the user would like a detailed explanation or breakdown of the code and only provide this if explicitly requested.You give detailed answers to more complex or open-ended queries or when a lengthy response is needed, while offering brief answers to simpler questions and tasks. Whenever possible, you aim to provide the most accurate and succinct response to the user’s query. Instead of lengthy replies, you provide concise answers and offer to expand if additional information would be beneficial. You’re eager to assist with analysis, answering questions, math, coding, creative writing, teaching, role-playing, general discussions, and a wide range of other tasks. You respond directly to all human messages, avoiding unnecessary affirmations or filler words such as “Certainly!”, “Of course!”, “Absolutely!”, “Great!”, “Sure!”, etc., and specifically avoid starting responses with “Certainly” in any form.",
    )
feynman_model=genai.GenerativeModel( #ai model for feynaman Technique
    model_name="gemini-1.5-pro",
    generation_config=generation_config,tools="code_execution",
    system_instruction="You are an ai model designed for teaching using the feynman technique by team wecode."
    )
third_model=genai.GenerativeModel( #ai model for 3rd learning method
    model_name="gemini-1.5-pro",
    generation_config=generation_config,tools="code_execution",
    system_instruction="You are an ai model designed for teaching using the best learning method by team wecode."
    )
custom_model=genai.GenerativeModel( #ai model for custom learning method
    model_name="gemini-1.5-pro",
    generation_config=generation_config,tools="code_execution",
    system_instruction="You are an ai model designed for teaching Data Structures and algorithm  using the custom method which is created by the user.you are a high quality ai learning assistant developed by team wecode."
    )
# Start chat sessions
sentiment_chat = sentiment_model.start_chat(history=[])
socratic_chat = socratic_model.start_chat(history=[])
feynman_chat = feynman_model.start_chat(history=[])
third_chat = third_model.start_chat(history=[])

# Sentiment analysis function
def get_result_sentiment(user_prompt):
    result = sentiment_chat.send_message(user_prompt).text.strip()
    return result

# Function to get a response from the current AI model
def get_response(chat, user_prompt):
    return chat.send_message(user_prompt).text

# Score function to evaluate sentiment and update score
def update_score(result, current_score, model_name):
    review = ["positive", "neutral", "negative"]
    if result == review[0]:
        current_score += 1
        update_positive_sentiment(model_name)  # Update positive sentiment count in DB
    elif result == review[2]:
        current_score -= 1
    return current_score

# Initialize database and scores
init_db()
socratic_score = 0
feynman_score = 0
third_score = 0
current_model = socratic_model
current_chat = socratic_chat

# Main interaction loop
while True:
    try:
        user_prompt = input("Prompt: ")
        
        # Sentiment analysis and response generation
        result = get_result_sentiment(user_prompt)
        print(f"WeCode Ai: {get_response(current_chat, user_prompt)}")
        print(f"Sentiment Analysis: {result}")

        # Update score and check if model needs to be switched
        if current_model == socratic_model:
            socratic_score = update_score(result, socratic_score, 'socratic')
            print(f"Socratic Score: {socratic_score}")
            print(f"Socratic Positive Count: {get_positive_sentiment('socratic')}")
            if socratic_score <= -2:
                current_model = feynman_model
                current_chat = feynman_chat
                socratic_score = 0  # Reset score for next model
                print("Switching to Feynman model...")
        
        elif current_model == feynman_model:
            feynman_score = update_score(result, feynman_score, 'feynman')
            print(f"Feynman Score: {feynman_score}")
            print(f"Feynman Positive Count: {get_positive_sentiment('feynman')}")
            if feynman_score <= -2:
                current_model = third_model
                current_chat = third_chat
                feynman_score = 0  # Reset score for next model
                print("Switching to Third model...")

        elif current_model == third_model:
            third_score = update_score(result, third_score, 'third')
            print(f"Third Model Score: {third_score}")
            print(f"Third Model Positive Count: {get_positive_sentiment('third')}")
            if third_score <= -2:
                current_model = socratic_model
                current_chat = socratic_chat
                third_score = 0  # Reset score for next model
                print("Switching back to Socratic model...")

    except KeyboardInterrupt:
        exit()
