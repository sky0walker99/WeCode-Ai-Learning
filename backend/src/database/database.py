import sqlite3
from datetime import datetime, timedelta
import os
from config.config import *



# Initialize the database 
def init_db():
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
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

#Function for clearing the database
def clear_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear data from ChatHistory
    cursor.execute("DELETE FROM ChatHistory")

    # Clear data from SentimentCount and reset values
    cursor.execute("DELETE FROM SentimentCount")
    cursor.execute("""
        INSERT INTO SentimentCount (model, positive_count) VALUES 
        ('socratic', 0),
        ('feynman', 0)
    """)

    conn.commit()
    conn.close()



