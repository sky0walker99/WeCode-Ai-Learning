import React, { useEffect, useState } from 'react';
import apiService from '../service/api.service'; // Assuming this is where getChatHistory is located

const ChatHistory = () => {
  const [messages, setMessages] = useState([]);

  // Fetch chat history from the API
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await apiService.getChatHistory();
        const history = response.data.chat_history; // Get the 'chat_history' array from the response

        const transformedMessages = history.map((entry) => [
          { sender: 'user', text: entry.user_message, timestamp: entry.timestamp },
          { sender: 'bot', text: entry.ai_response, timestamp: entry.timestamp }
        ]).flat(); // Flatten the array to keep user and bot messages in order

        setMessages(transformedMessages); // Set the messages in state
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    fetchChatHistory();
  }, [messages]);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100 w-full">
      <div className="w-full max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Chat History */}
        <div className="p-4 h-96 overflow-y-auto">
          {messages.map((message, index) => (
            <div key={index} className={`flex mb-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'} p-3 rounded-lg max-w-xs`}>
                <div>{message.text}</div>
                <div className="text-xs text-gray-500 mt-1"> {new Date(message.timestamp).toLocaleDateString()} {new Date(message.timestamp).toLocaleTimeString()}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatHistory;
