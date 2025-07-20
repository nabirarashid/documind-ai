import { useState, useRef } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
    onSendMessage: (message: string) => void;
    isLoading: boolean;
}

const ChatInput = ({ onSendMessage, isLoading }: ChatInputProps) => {
  const [message, setMessage] = useState('');
  const inputRef = useRef(null);

  const handleSubmit = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

interface KeyPressEvent {
    key: string;
    shiftKey: boolean;
    preventDefault: () => void;
}

const handleKeyPress = (e: KeyPressEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
    }
};

  return (
    <div className="relative">
      <div className="flex items-center space-x-2 bg-white rounded-full border-2 border-gray-200 focus-within:border-blue-500 transition-colors duration-200 p-2">
        <input
          ref={inputRef}
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask anything about the documentation..."
          className="flex-1 bg-transparent px-4 py-3 text-gray-700 placeholder-gray-400 focus:outline-none"
          disabled={isLoading}
        />
        <button
          onClick={handleSubmit}
          disabled={!message.trim() || isLoading}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full p-3 hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 hover:scale-105"
        >
          <Send className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;