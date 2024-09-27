import React, { useEffect, useState, useRef } from 'react';
import apiService from '../service/api.service';

const ChatApp = ({ model }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const messageEndRef = useRef(null);

  const handleSendMessage = () => {
    if (inputValue.trim() === '' && !selectedFile) return;

    // Add the message and file to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        sender: 'user',
        text: inputValue,
        file: selectedFile ? selectedFile.name : null,
      },
    ]);

    const inputDetails = {
      "user_input" : inputValue,
    }

    apiService.postInputData(inputDetails).then((data) => {
      console.log('data');
      console.log(data);
    });

    // Reset input and file selection
    setInputValue('');
    setSelectedFile(null);
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  useEffect(() => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100 w-full">
      <div className="w-full max-w-md bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Chat Window */}
        <div className="p-4 h-96 overflow-y-auto">
          {messages.map((message, index) => (
            <div key={index} className={`flex mb-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`${message.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-300 text-black'} p-3 rounded-lg max-w-xs`}>
                {message.text}
                {message.file && (
                  <div className="mt-2 text-sm text-gray-600">
                    <span className="font-bold">Attached File: </span>{message.file}
                  </div>
                )}
              </div>
            </div>
          ))}
          <div ref={messageEndRef} />
        </div>

        {/* Input Box */}
        <div className="flex items-center border-t p-4">
          {/* Text Input */}
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type a message..."
            className="flex-grow p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          {/* File Input */}
          <label className="ml-2 px-3 py-2 bg-gray-200 text-gray-600 rounded-md cursor-pointer hover:bg-gray-300 focus:outline-none">
            <input
              type="file"
              onChange={handleFileChange}
              className="hidden"
            />
            📎
          </label>

          {/* Send Button */}
          <button
            onClick={handleSendMessage}
            className="ml-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none"
          >
            Send
          </button>
        </div>

        {/* Display Selected File */}
        {selectedFile && (
          <div className="p-2 text-sm text-gray-700">
            <span className="font-bold">Selected File: </span>{selectedFile.name}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatApp;
