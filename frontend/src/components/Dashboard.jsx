import { useState } from 'react';
import { 
  AcademicCapIcon, 
  DocumentTextIcon, 
  QuestionMarkCircleIcon, 
  ChatBubbleLeftRightIcon,
  BookOpenIcon,
  PuzzlePieceIcon,
  ChartBarIcon,
  CogIcon,
  BellIcon,
  UserCircleIcon,
  ArrowLeftOnRectangleIcon,
  HomeIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/api';
import ContentGeneratorForm from './ContentGeneratorForm';

const Dashboard = ({ user, onLogout }) => {
  const [activeView, setActiveView] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isGeneratingContent, setIsGeneratingContent] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [contentHistory, setContentHistory] = useState([]);

  const navigationItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: HomeIcon,
      description: 'Overview and statistics'
    },
    {
      id: 'content-generator',
      name: 'Content Generator',
      icon: DocumentTextIcon,
      description: 'Generate learning content and materials',
      color: 'blue'
    },
    {
      id: 'question-setter',
      name: 'Question Setter',
      icon: QuestionMarkCircleIcon,
      description: 'Create quizzes and assessments',
      color: 'green'
    },
    {
      id: 'feedback-evaluator',
      name: 'Feedback Evaluator',
      icon: ChatBubbleLeftRightIcon,
      description: 'Evaluate and provide feedback',
      color: 'purple'
    }
  ];

  const getColorClasses = (color) => {
    const colorMap = {
      blue: {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-700',
        hover: 'hover:bg-blue-100',
        icon: 'text-blue-600',
        light: 'bg-blue-100'
      },
      green: {
        bg: 'bg-green-50',
        border: 'border-green-200',
        text: 'text-green-700',
        hover: 'hover:bg-green-100',
        icon: 'text-green-600',
        light: 'bg-green-100'
      },
      purple: {
        bg: 'bg-purple-50',
        border: 'border-purple-200',
        text: 'text-purple-700',
        hover: 'hover:bg-purple-100',
        icon: 'text-purple-600',
        light: 'bg-purple-100'
      }
    };
    return colorMap[color] || colorMap.blue;
  };

  const handleContentGeneration = async (formData) => {
    setIsGeneratingContent(true);
    
    try {
      // Send content generation request to backend
      const response = await apiService.generateContent({
        topic: formData.topic,
        difficulty_level: formData.difficultyLevel,
        content_type: formData.contentType
      });
      
      // Store the response in state
      setGeneratedContent({
        id: response.id,
        topic: response.topic,
        difficultyLevel: response.difficulty_level,
        contentType: response.content_type,
        content: response.generated_content || `Content generation request submitted for ${response.topic}. The AI agent will process this and generate content shortly.`,
        timestamp: response.request_timestamp,
        status: response.status
      });
      
      // Add to content history
      setContentHistory(prev => [{
        id: response.id,
        topic: response.topic,
        difficultyLevel: response.difficulty_level,
        contentType: response.content_type,
        content: response.generated_content || 'Content generation in progress...',
        timestamp: response.request_timestamp,
        status: response.status
      }, ...prev]);
      
      console.log(`✅ Content generation request submitted successfully: ${response.id}`);
      
    } catch (error) {
      console.error('Error generating content:', error);
      // TODO: Show user-friendly error message
      alert('Failed to submit content generation request. Please try again.');
    } finally {
      setIsGeneratingContent(false);
    }
  };

  const handleLogout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('authToken');
      onLogout();
    }
  };

  const renderDashboardContent = () => (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.first_name || 'Student'}! 👋
        </h1>
        <p className="text-gray-600">
          Choose an AI tutor to start your learning session or continue where you left off.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BookOpenIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Sessions Today</p>
              <p className="text-2xl font-semibold text-gray-900">3</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <ChartBarIcon className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Progress</p>
              <p className="text-2xl font-semibold text-gray-900">78%</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <PuzzlePieceIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Problems Solved</p>
              <p className="text-2xl font-semibold text-gray-900">24</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <ChatBubbleLeftRightIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Questions Asked</p>
              <p className="text-2xl font-semibold text-gray-900">47</p>
            </div>
          </div>
        </div>
      </div>

      {/* AI Agents Section */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Your AI Learning Partners</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {navigationItems.slice(1).map((agent) => {
            const colors = getColorClasses(agent.color);
            const IconComponent = agent.icon;
            
            return (
              <div
                key={agent.id}
                className={`bg-white rounded-xl shadow-sm border-2 ${colors.border} hover:shadow-md transition-all duration-200 cursor-pointer group ${colors.hover}`}
                onClick={() => setActiveView(agent.id)}
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-lg ${colors.bg}`}>
                      <IconComponent className={`h-8 w-8 ${colors.icon}`} />
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 rounded-full bg-green-500"></div>
                      <span className="text-xs text-gray-500">Online</span>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{agent.name}</h3>
                  <p className="text-gray-600 mb-4">{agent.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <button className={`px-4 py-2 rounded-lg ${colors.bg} ${colors.text} font-medium text-sm transition-colors group-hover:bg-opacity-80`}>
                      Start Session
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Learning Activity</h3>
        <div className="space-y-4">
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="p-2 bg-blue-100 rounded-lg">
              <DocumentTextIcon className="h-5 w-5 text-blue-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Generated: Linear Algebra Study Guide</p>
              <p className="text-xs text-gray-500">2 hours ago with Content Generator</p>
            </div>
            <span className="text-xs text-green-600 font-medium">Completed</span>
          </div>
          
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="p-2 bg-green-100 rounded-lg">
              <QuestionMarkCircleIcon className="h-5 w-5 text-green-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Quiz Created: Quadratic Equations</p>
              <p className="text-xs text-gray-500">4 hours ago with Question Setter</p>
            </div>
            <span className="text-xs text-blue-600 font-medium">In Progress</span>
          </div>
          
          <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
            <div className="p-2 bg-purple-100 rounded-lg">
              <ChatBubbleLeftRightIcon className="h-5 w-5 text-purple-600" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-900">Feedback: Calculus Derivatives</p>
              <p className="text-xs text-gray-500">1 day ago with Feedback Evaluator</p>
            </div>
            <span className="text-xs text-green-600 font-medium">Score: 85%</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderContentGenerator = () => (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-4 mb-6">
          <div className="p-4 bg-blue-100 rounded-lg">
            <DocumentTextIcon className="h-12 w-12 text-blue-600" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Content Generator</h1>
            <p className="text-gray-600 text-lg">Generate personalized learning content tailored to your needs</p>
          </div>
        </div>
      </div>

      {/* Content Generation Form */}
      <ContentGeneratorForm 
        onSubmit={handleContentGeneration}
        isLoading={isGeneratingContent}
      />

      {/* Generated Content Display */}
      {generatedContent && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Generated Content</h3>
            <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
              {generatedContent.status}
            </span>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4 mb-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-700">Topic:</span>
                <p className="text-gray-600">{generatedContent.topic}</p>
              </div>
              <div>
                <span className="font-medium text-gray-700">Difficulty:</span>
                <p className="text-gray-600 capitalize">{generatedContent.difficultyLevel}</p>
              </div>
              <div>
                <span className="font-medium text-gray-700">Type:</span>
                <p className="text-gray-600 capitalize">{generatedContent.contentType.replace('-', ' ')}</p>
              </div>
            </div>
          </div>
          
          <div className="prose max-w-none">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">Content:</h4>
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              <p className="text-gray-700 leading-relaxed">{generatedContent.content}</p>
            </div>
          </div>
          
          <div className="mt-4 text-sm text-gray-500">
            Generated on {new Date(generatedContent.timestamp).toLocaleString()}
          </div>
        </div>
      )}

      {/* Content History */}
      {contentHistory.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Content History</h3>
          <div className="space-y-3">
            {contentHistory.slice(1).map((content) => (
              <div key={content.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <DocumentTextIcon className="h-5 w-5 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-900">{content.topic}</p>
                    <p className="text-xs text-gray-500">
                      {content.contentType.replace('-', ' ')} • {content.difficultyLevel} • {new Date(content.timestamp).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setGeneratedContent(content)}
                  className="px-3 py-1 text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded-md transition-colors"
                >
                  View
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  const renderAgentContent = (agentId) => {
    const agent = navigationItems.find(item => item.id === agentId);
    if (!agent) return null;

    // Special handling for Content Generator
    if (agentId === 'content-generator') {
      return renderContentGenerator();
    }

    const colors = getColorClasses(agent.color);
    const IconComponent = agent.icon;

    return (
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center space-x-4 mb-6">
            <div className={`p-4 rounded-lg ${colors.bg}`}>
              <IconComponent className={`h-12 w-12 ${colors.icon}`} />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{agent.name}</h1>
              <p className="text-gray-600 text-lg">{agent.description}</p>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Getting Started</h3>
            <p className="text-gray-600 mb-4">
              This AI agent is ready to help you with your learning journey. 
              Start a session to begin interacting with {agent.name}.
            </p>
            <button className={`px-6 py-3 rounded-lg ${colors.bg} ${colors.text} font-medium transition-colors hover:bg-opacity-80`}>
              Start New Session
            </button>
          </div>
        </div>

        {/* Placeholder for agent-specific content */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Session History</h3>
          <div className="text-center py-12 text-gray-500">
            <IconComponent className="h-16 w-16 mx-auto mb-4 text-gray-300" />
            <p>No sessions yet. Start your first session to see your history here.</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 mr-3 lg:hidden"
              >
                <Bars3Icon className="h-6 w-6" />
              </button>
              <AcademicCapIcon className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">TutorMind AI</span>
            </div>
            
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-500">
                <BellIcon className="h-6 w-6" />
              </button>
              <button className="p-2 text-gray-400 hover:text-gray-500">
                <CogIcon className="h-6 w-6" />
              </button>
              
              {/* User Menu */}
              <div className="relative">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center space-x-2">
                    {user?.avatar ? (
                      <img src={user.avatar} alt="Avatar" className="h-8 w-8 rounded-full" />
                    ) : (
                      <UserCircleIcon className="h-8 w-8 text-gray-400" />
                    )}
                    <span className="text-sm font-medium text-gray-700">{user?.first_name || user?.name || 'User'}</span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="p-2 text-gray-400 hover:text-gray-500"
                    title="Logout"
                  >
                    <ArrowLeftOnRectangleIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}>
          <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200 lg:hidden">
            <span className="text-lg font-semibold text-gray-900">Navigation</span>
            <button
              onClick={() => setSidebarOpen(false)}
              className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>
          
          <nav className="mt-6 px-3">
            <div className="space-y-1">
              {navigationItems.map((item) => {
                const IconComponent = item.icon;
                const isActive = activeView === item.id;
                const colors = item.color ? getColorClasses(item.color) : null;
                
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveView(item.id);
                      setSidebarOpen(false);
                    }}
                    className={`w-full flex items-center px-3 py-3 text-sm font-medium rounded-lg transition-colors ${
                      isActive
                        ? colors
                          ? `${colors.bg} ${colors.text} ${colors.border} border`
                          : 'bg-gray-100 text-gray-900'
                        : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }`}
                  >
                    <IconComponent className={`h-5 w-5 mr-3 ${
                      isActive && colors ? colors.icon : 'text-gray-400'
                    }`} />
                    {item.name}
                  </button>
                );
              })}
            </div>
          </nav>
        </div>

        {/* Main Content */}
        <main className="flex-1 lg:ml-0">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {activeView === 'dashboard' ? renderDashboardContent() : renderAgentContent(activeView)}
          </div>
        </main>
      </div>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
