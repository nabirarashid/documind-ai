import { useState, useRef, useEffect } from "react";
import { Sparkles, MessageSquare } from "lucide-react";
import ChatInput from "./ChatInput";
import Message from "./Message";
import { db } from "../lib/firebase";
import { collection, addDoc, Timestamp } from "firebase/firestore";
import { useAuth } from "../contexts/AuthContext";

const ChatInterface = () => {

  const { user } = useAuth();
  
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      text: "Hi! I'm your documentation assistant. I can help you find information about APIs, code examples, and technical documentation. What would you like to know?",
      isBot: true,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const chatRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  interface ChatMessage {
    id: number;
    text: string;
    isBot: boolean;
    sources?: Array<{
      tool: string;
      title: string;
      url: string;
      snippet: string;
    }>;
  }

  const handleSendMessage = async (messageText: string): Promise<void> => {
    const newMessage: ChatMessage = {
      id: messages.length + 1,
      text: messageText,
      isBot: false,
    };

    setMessages((prev: ChatMessage[]) => [...prev, newMessage]);
    setIsLoading(true);

    try {
      // Use environment variable for API URL
      const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      // saving user query to Firestore
      if (user) {
        await addDoc(collection(db, "user searches"), {
          uid: user.uid,
          query: messageText,
          timestamp: Timestamp.now(),
        });
      }

      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: messageText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Create sources from the context chunks (if available)
      const sources = data.sources || [];

      const botResponse: ChatMessage = {
        id: messages.length + 2,
        text: data.answer || "Sorry, I couldn't get a response right now.",
        isBot: true,
        sources: sources,
      };

      setMessages((prev: ChatMessage[]) => [...prev, botResponse]);
    } catch (error) {
      console.error("Error calling backend:", error);

      const errorResponse: ChatMessage = {
        id: messages.length + 2,
        text: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running and try again.",
        isBot: true,
      };

      setMessages((prev: ChatMessage[]) => [...prev, errorResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden max-w-5xl mx-auto">
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4">
        <div className="flex items-center space-x-3">
          <MessageSquare className="h-6 w-6 text-white" />
          <h3 className="font-bold text-white text-lg">
            Documentation Assistant
          </h3>
          <div className="ml-auto flex items-center space-x-2">
            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            <span className="text-white text-sm">Online</span>
          </div>
        </div>
      </div>

      <div
        ref={chatRef}
        className="h-[500px] overflow-y-auto p-6 bg-gradient-to-b from-gray-50 to-white"
      >
        {messages.map((msg) => (
          <Message
            key={msg.id}
            message={msg.text}
            isBot={msg.isBot}
            sources={msg.sources}
          />
        ))}

        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 max-w-[80%]">
              <div className="flex items-center space-x-2">
                <Sparkles className="h-4 w-4 text-blue-500 animate-pulse" />
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="p-6 border-t border-gray-200 bg-white">
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default ChatInterface;
