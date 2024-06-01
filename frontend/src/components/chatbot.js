import React, { useState } from 'react';
import '../styles/chatbot.css';
import axios from 'axios';
import BotIcon from './boticon.svg';
import Spinner from './spinner.svg';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleMessageSubmit = async () => {
    if (inputValue.trim() === '') return;
    setMessages([...messages, { text: inputValue, sender: 'user' }]);
    setInputValue('');
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/query', { question: inputValue });
      const answer = response.data.answer;
      setMessages(prevMessages => [
        ...prevMessages,
        { text: answer, sender: 'bot' }
      ]);
    } catch (error) {
      console.error('Error sending query:', error);
      setMessages(prevMessages => [
        ...prevMessages,
        { text: 'An error occurred. Please try again later.', sender: 'bot' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  return (
    <div className="chatbot-container">
      <div className="messages-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="circle">{message.sender === 'user' ? 'U' : <img src={BotIcon} alt="Bot" />}</div>
            <div className="text">{message.text}</div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="circle"><img src={BotIcon} alt="Bot" /></div>
            <div className="text"><img src={Spinner} alt="Loading..." className="spinner" /></div>
          </div>
        )}
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Send a message..."
          value={inputValue}
          onChange={handleInputChange}
        />
        <button className="send-button" onClick={handleMessageSubmit}>
          <svg width="19" height="16" viewBox="0 0 19 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.1667 7.99999L0.75 15.3333L4.01608 7.99999L0.75 0.666656L18.1667 7.99999ZM18.1667 7.99999H3.95833" stroke="#222222" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default Chatbot;
