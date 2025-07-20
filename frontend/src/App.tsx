import { Search, Zap, Brain } from 'lucide-react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import FeatureCard from './components/FeatureCard';
import Footer from './components/Footer';
import { AuthProvider } from './contexts/AuthContext';

const App = () => {
  return (
    <AuthProvider>
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
       
        
        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <FeatureCard
            icon={Search}
            title="Smart Search"
            description="AI-powered semantic search through documentation using advanced embeddings"
            gradient="bg-gradient-to-br from-blue-500 to-blue-600"
          />
          <FeatureCard
            icon={Zap}
            title="Lightning Fast"
            description="Powered by Gemini Flash for ultra-fast responses and cost-effective queries"
            gradient="bg-gradient-to-br from-purple-500 to-purple-600"
          />
          <FeatureCard
            icon={Brain}
            title="Context Aware"
            description="RAG architecture ensures responses are grounded in your actual documentation"
            gradient="bg-gradient-to-br from-indigo-500 to-indigo-600"
          />
        </div>

        {/* Main Chat Interface */}
        <div className="mb-8">
          <div className="text-center mb-6">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Chat with Your Documentation</h2>
            <p className="text-gray-600">Ask questions and get instant, accurate answers from your docs</p>
          </div>
          <ChatInterface />
        </div>
        <Footer />  
      </main>
    </div>
    </AuthProvider>
  );
}

export default App
