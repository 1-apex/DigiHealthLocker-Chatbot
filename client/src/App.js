import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import 'tailwindcss/tailwind.css';
import './index.css';
import { IoSend } from "react-icons/io5";
import { BsRobot } from "react-icons/bs";
import img1 from './assets/images/png-transparent-cartoon-hospital-medical-medical-mark-icon-thumbnail-removebg-preview.png';
import img2 from './assets/images/pngtree-hand-painted-medical-icon-medical-png-image_3774841-removebg-preview.png'


const socket = io();

const App = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const [feedback, setFeedback] = useState('');

  useEffect(() => {
    socket.on('update_bot_response', (data) => {
      addMessageToUI(false, data);
    });

    socket.on('feedback-message', (data) => {
      setFeedback(data.feedback);
    });

    return () => {
      socket.off('update_bot_response');
      socket.off('feedback-message');
    };
  }, []);

  const sendMessage = () => {
    if (message === '') return;

    const data = {
      message: message,
      dateTime: new Date()
    };

    socket.emit('client_message', data);
    addMessageToUI(true, data);
    setMessage('');
  };

  const addMessageToUI = (isOwnMessage, data) => {
    setFeedback('');
    setMessages((prevMessages) => [
      ...prevMessages,
      { isOwnMessage: isOwnMessage, ...data }
    ]);
  };

  const handleFocus = () => {
    socket.emit('feedback', {
      feedback: `E-Doc is typing...`
    });
  };

  const handleBlur = () => {
    socket.emit('feedback', {
      feedback: ``
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  return (
    <div className="flex justify-between items-center min-h-screen bg-gray-200">
      <img className='h-60 opacity-70' src={img1} alt='health-related-img1'/>
      <div className='mr-32 mb-36'>
      <img className='ml-24 h-40 mb-5 opacity-70' src={img2} alt='health-related-img2'/>
      <h1 className="text-7xl font-bold text-teal-800">DigiHealthLocker</h1>
      <h1 className="text-6xl font-bold mt-4 text-teal-700">ChatBot</h1>
      <p className='text-xl font-bold mt-4 text-gray-600'>Bridging the Gap Between You and Your Doctor</p>
      </div>
      <div className="border-8 border-gray-300 rounded-2xl overflow-hidden w-full max-w-md bg-white shadow-lg mr-52">
        <div className="flex items-center p-4 bg-gray-200 text-gray-700 font-bold">
          <BsRobot size={24} />
          <p className='ml-2 text-2xl'>E-Doc</p>
        </div>

        <ul className="flex flex-col bg-gray-100 h-96 overflow-y-auto p-4" id="message-container">
          <li className="self-start p-3 mb-3 bg-white rounded-2xl shadow-sm max-w-xs text-teal-800">
            <p className=''>Hi, I am EDoc - DigiHealthLocker Bot assistant. How can I assist you today?</p>
          </li>
          {messages.map((msg, index) => (
            <li
              key={index}
              className={`p-3 mb-3 rounded-2xl shadow-sm max-w-xs ${msg.isOwnMessage ? 'self-end bg-teal-800 text-white' : 'self-start bg-white'}`}
            >
              <p>{msg.message}</p>
            </li>
          ))}
          {feedback && (
            <li className="self-start p-3 mb-3 text-sm italic text-teal-800 bg-gray-100 rounded-2xl">
              {feedback}
            </li>
          )}
        </ul>

        <form className="flex justify-between p-4 bg-white border-t" id="message-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="message"
            id="message-input"
            className="flex-grow h-12 p-3 text-lg border-none outline-none bg-gray-100"
            placeholder="Ask me about any medicine..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onFocus={handleFocus}
            onBlur={handleBlur}
          />
          <div className="w-px h-12 bg-gray-200 mx-2"></div>
          <button type="submit" className="h-12 px-6 text-lg bg-gray-100 border-none cursor-pointer">
            <IoSend size={24} /><span><i className="fas fa-paper-plane"></i></span>
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
