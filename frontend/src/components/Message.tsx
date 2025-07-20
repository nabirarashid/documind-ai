import { Sparkles } from "lucide-react";
import { SourceReferences } from "./Source";

interface MessageProps {
  message: string;
  isBot: boolean;
  sources?: Array<{
    tool: string;
    title: string;
    url: string;
    snippet: string;
  }>;
}

const Message = ({ message, isBot, sources }: MessageProps) => (
  <div className={`flex ${isBot ? "justify-start" : "justify-end"} mb-4`}>
    <div
      className={`max-w-[80%] rounded-2xl px-4 py-3 ${
        isBot
          ? "bg-gray-100 text-gray-800 rounded-bl-sm"
          : "bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-br-sm"
      }`}
    >
      {isBot && (
        <div className="flex items-center mb-2">
          <Sparkles className="h-4 w-4 mr-2" />
          <span className="text-xs font-medium text-gray-600">DocuMind AI</span>
        </div>
      )}
      <p className="text-sm leading-relaxed">{message}</p>

      {/* Show sources for bot messages */}
      {isBot && sources && sources.length > 0 && (
        <SourceReferences sources={sources} className="mt-3" />
      )}
    </div>
  </div>
);

export default Message;
