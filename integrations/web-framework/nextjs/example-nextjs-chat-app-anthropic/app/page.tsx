'use client';

import { useEffect, useRef, useState } from 'react';

interface Message {
  user: string;
  text: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const chatBox = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatBox.current?.lastElementChild?.scrollIntoView({ behavior: 'smooth' });
  }, [messages])

  const handleSendMessage = async (e: any) => {
    e.preventDefault();
    if (input.trim()) {
      const newMessages = [...messages, { user: 'user', text: input }, { user: 'bot', text: 'Typing...' }];
      setMessages(newMessages);
      setInput('');

      try {
        const allMessages = newMessages.reduce((acc, message) => acc + `${message.user === 'user' ? 'question: ' + message.text : 'answer: ' + message.text}` + '\n\n', '');
        const trimmedMessages = allMessages.slice(-8000);
        const response = await fetch('/api/chat', {body: JSON.stringify({ message: trimmedMessages }), method: 'POST', headers: { 'Content-Type': 'application/json' }});
        const reply = await response.json();
        const displayedMessages = newMessages.slice(0, -1);
        setMessages([...displayedMessages, { user: 'bot', text: reply }]);
        
      } catch (error) {
        console.error('Error fetching response:', error);
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">Ask me anything.</h1>
        <div ref={chatBox} className="flex flex-col space-y-4 mb-4 h-96 overflow-y-scroll border border-gray-300 p-4 rounded-lg">
          {messages.map((message, index) => (
            <div key={index} className={`flex ${message.user === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`${
                  message.user === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-900'
                } p-3 rounded-lg max-w-xs`}
              >
                <p>{message.text}</p>
              </div>
            </div>
          ))}
        </div>
        <form onSubmit={handleSendMessage} className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="flex-grow p-2 border border-gray-300 rounded-l-lg focus:outline-none"
            placeholder="Type your message..."
          />
          <button
            className="p-2 bg-blue-500 text-white rounded-r-lg hover:bg-blue-600 focus:outline-none"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
