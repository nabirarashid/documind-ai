import { Zap, Brain, User, LogOut } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";
import { Login } from "./Login";
import { useState } from "react";

const Header = () => {
  const { user, logout } = useAuth();
  const [showLogin, setShowLogin] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <>
      <header className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-white/20 backdrop-blur-sm rounded-lg p-2">
                <Brain className="h-8 w-8" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">DocuMind AI</h1>
                <p className="text-blue-100">
                  Intelligent Documentation Assistant
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="hidden md:flex items-center space-x-2 bg-white/10 rounded-full px-3 py-1">
                <Zap className="h-4 w-4" />
                <span className="text-sm">Powered by Gemini Flash</span>
              </div>

              {user ? (
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2 bg-white/10 rounded-full px-3 py-2">
                    <User className="h-4 w-4" />
                    <span className="text-sm">{user.email}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-1 bg-white/10 hover:bg-white/20 rounded-full px-3 py-2 transition-colors"
                    title="Logout"
                  >
                    <LogOut className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowLogin(true)}
                  className="bg-white/10 hover:bg-white/20 rounded-full px-4 py-2 transition-colors flex items-center space-x-2"
                >
                  <User className="h-4 w-4" />
                  <span>Sign In</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {showLogin && <Login onClose={() => setShowLogin(false)} />}
    </>
  );
};

export default Header;
