import React from 'react';

const ChatHistory = () => {
  const messages = [
    { sender: 'user', text: 'Hello, can you help me?' },
    { sender: 'bot', text: 'Of course! What do you need assistance with?' },
    // Add more static or dynamic messages as needed
  ];

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100 w-full">
      <div className="w-full max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Chat History */}
        <div className="p-4 h-96 overflow-y-auto">
          {messages.map((message, index) => (
            <div key={index} className={`flex mb-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'} p-3 rounded-lg max-w-xs`}>
                {message.text}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatHistory;
