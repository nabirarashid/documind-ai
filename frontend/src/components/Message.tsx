import { Sparkles } from 'lucide-react';

interface MessageProps {
    message: string;
    isBot: boolean;
}

const Message = ({ message, isBot }: MessageProps) => (
  <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}>
    <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
      isBot 
        ? 'bg-gray-100 text-gray-800 rounded-bl-sm' 
        : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-br-sm'
    }`}>
      {isBot && (
        <div className="flex items-center mb-2">
          <Sparkles className="h-4 w-4 mr-2" />
          <span className="text-xs font-medium text-gray-600">DocuMind AI</span>
        </div>
      )}
      <p className="text-sm leading-relaxed">{message}</p>
    </div>
  </div>
);

export default Message;