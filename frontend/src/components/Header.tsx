import { Zap, Brain } from 'lucide-react';

const Header = () => (
  <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white">
    <div className="max-w-7xl mx-auto px-4 py-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-white/20 backdrop-blur-sm rounded-lg p-2">
            <Brain className="h-8 w-8" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">DocuMind AI</h1>
            <p className="text-blue-100">Intelligent Documentation Assistant</p>
          </div>
        </div>
        <div className="hidden md:flex items-center space-x-6">
          <div className="flex items-center space-x-2 bg-white/10 rounded-full px-3 py-1">
            <Zap className="h-4 w-4" />
            <span className="text-sm">Powered by Gemini Flash</span>
          </div>
        </div>
      </div>
    </div>
  </header>
);

export default Header;