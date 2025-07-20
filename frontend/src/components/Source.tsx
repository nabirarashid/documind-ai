import React from 'react';
import { ExternalLink, Book, Palette, Code, Cloud, CreditCard } from 'lucide-react';

interface Source {
  tool: string;
  title: string;
  url: string;
  snippet: string;
}

interface SourceReferencesProps {
  sources: Source[];
  className?: string;
}

const getToolIcon = (toolName: string) => {
  const tool = toolName.toLowerCase();
  switch (tool) {
    case 'stripe':
      return <CreditCard className="w-4 h-4" />;
    case 'tailwind':
    case 'tailwindcss':
      return <Palette className="w-4 h-4" />;
    case 'react':
    case 'nextjs':
    case 'next.js':
      return <Code className="w-4 h-4" />;
    case 'vercel':
      return <Cloud className="w-4 h-4" />;
    default:
      return <Book className="w-4 h-4" />;
  }
};

const getToolColor = (toolName: string) => {
  const tool = toolName.toLowerCase();
  switch (tool) {
    case 'stripe':
      return 'bg-purple-50 border-purple-200 text-purple-800';
    case 'tailwind':
    case 'tailwindcss':
      return 'bg-cyan-50 border-cyan-200 text-cyan-800';
    case 'react':
      return 'bg-blue-50 border-blue-200 text-blue-800';
    case 'nextjs':
    case 'next.js':
      return 'bg-gray-50 border-gray-200 text-gray-800';
    case 'vercel':
      return 'bg-black text-white border-gray-800';
    default:
      return 'bg-green-50 border-green-200 text-green-800';
  }
};

export const SourceReferences: React.FC<SourceReferencesProps> = ({ 
  sources, 
  className = "" 
}) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  // Group sources by tool for better organization
  const groupedSources = sources.reduce((acc, source) => {
    if (!acc[source.tool]) {
      acc[source.tool] = [];
    }
    acc[source.tool].push(source);
    return acc;
  }, {} as Record<string, Source[]>);

  return (
    <div className={`mt-4 ${className}`}>
      <div className="flex items-center gap-2 mb-3">
        <Book className="w-4 h-4 text-gray-500" />
        <span className="text-sm font-medium text-gray-700">Sources</span>
      </div>
      
      <div className="space-y-3">
        {Object.entries(groupedSources).map(([tool, toolSources]) => (
          <div key={tool} className="space-y-2">
            {/* Tool Header */}
            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium border ${getToolColor(tool)}`}>
              {getToolIcon(tool)}
              <span className="capitalize">{tool}</span>
            </div>
            
            {/* Sources for this tool */}
            <div className="ml-2 space-y-2">
              {toolSources.map((source, index) => (
                <div 
                  key={`${tool}-${index}`}
                  className="group bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {source.title || 'Documentation'}
                      </h4>
                      {source.snippet && (
                        <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                          {source.snippet.substring(0, 120)}...
                        </p>
                      )}
                    </div>
                    
                    {source.url && (
                      <a 
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex-shrink-0 p-1 text-gray-400 hover:text-gray-600 transition-colors"
                        title="Open source"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Compact version for inline use
export const CompactSourceReferences: React.FC<SourceReferencesProps> = ({ 
  sources, 
  className = "" 
}) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  const uniqueTools = [...new Set(sources.map(s => s.tool))];

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <span className="text-xs text-gray-500">Sources:</span>
      <div className="flex gap-1">
        {uniqueTools.map((tool) => (
          <div 
            key={tool}
            className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs ${getToolColor(tool)}`}
          >
            {getToolIcon(tool)}
            <span className="capitalize">{tool}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SourceReferences;