import { Search, Zap, Brain } from 'lucide-react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import FeatureCard from './components/FeatureCard';

const App = () => {
  return (
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

        {/* Secondary Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-2xl p-6 border border-gray-200">
            <h3 className="font-semibold text-gray-800 mb-4 flex items-center">
              <Search className="h-5 w-5 mr-2 text-blue-600" />
              Popular Topics
            </h3>
            <div className="space-y-3">
              {[
                'API Authentication & Security',
                'Webhook Integration Patterns',
                'Rate Limiting & Throttling',
                'Error Handling Best Practices',
                'SDK Usage Examples',
                'Payment Processing Flows'
              ].map((topic, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 hover:bg-blue-50 rounded-lg cursor-pointer transition-colors duration-200 border border-transparent hover:border-blue-200">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-sm text-gray-700 font-medium">{topic}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-emerald-600 text-white rounded-2xl p-6">
            <h3 className="font-semibold mb-4 flex items-center">
              <Zap className="h-5 w-5 mr-2" />
              System Performance
            </h3>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-green-100 mb-1">Cost per Query</p>
                <p className="text-2xl font-bold">$0.001</p>
              </div>
              <div>
                <p className="text-sm text-green-100 mb-1">Average Response Time</p>
                <p className="text-2xl font-bold">1.2s</p>
              </div>
              <div>
                <p className="text-sm text-green-100 mb-1">Accuracy Rate</p>
                <p className="text-2xl font-bold">94%</p>
              </div>
            </div>
            <div className="mt-4 text-xs bg-white/20 rounded-full px-3 py-2 inline-block">
              Powered by open-source tools + Gemini Flash
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App
