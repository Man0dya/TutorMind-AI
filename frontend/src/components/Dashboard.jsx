import { useState } from 'react';
import { 
  AcademicCapIcon, 
  LightBulbIcon, 
  UserGroupIcon, 
  ArrowRightIcon,
  ChatBubbleLeftRightIcon,
  BookOpenIcon,
  PuzzlePieceIcon,
  ChartBarIcon,
  CogIcon,
  BellIcon,
  UserCircleIcon,
  ArrowLeftOnRectangleIcon
} from '@heroicons/react/24/outline';
import apiService from '../services/api';

const Dashboard = ({ user, onLogout }) => {
  const [activeAgent, setActiveAgent] = useState(null);

  const agents = [
    {
      id: 'concept-master',
      name: 'Concept Master',
      description: 'Break down complex topics into simple concepts',
      icon: AcademicCapIcon,
      color: 'blue',
      features: ['Theory & Concepts', 'Examples & Analogies', 'Fundamental Building Blocks'],
      status: 'online'
    },
    {
      id: 'problem-solver',
      name: 'Problem Solver',
      description: 'Guide you through step-by-step problem solutions',
      icon: LightBulbIcon,
      color: 'green',
      features: ['Step-by-step Solutions', 'Problem Strategies', 'Critical Thinking'],
      status: 'online'
    },
    {
      id: 'practice-coach',
      name: 'Practice Coach',
      description: 'Create personalized practice exercises and track progress',
      icon: UserGroupIcon,
      color: 'purple',
      features: ['Custom Exercises', 'Progress Tracking', 'Adaptive Learning'],
      status: 'online'
    }
  ];

  const getColorClasses = (color) => {
    const colorMap = {
      blue: {
        bg: 'bg-blue-50',
        border: 'border-blue-200',
        text: 'text-blue-700',
        hover: 'hover:bg-blue-100',
        icon: 'text-blue-600'
      },
      green: {
        bg: 'bg-green-50',
        border: 'border-green-200',
        text: 'text-green-700',
        hover: 'hover:bg-green-100',
        icon: 'text-green-600'
      },
      purple: {
        bg: 'bg-purple-50',
        border: 'border-purple-200',
        text: 'text-purple-700',
        hover: 'hover:bg-purple-100',
        icon: 'text-purple-600'
      }
    };
    return colorMap[color] || colorMap.blue;
  };

  const handleAgentClick = (agentId) => {
    setActiveAgent(agentId);
    // Here you would typically open a chat interface or redirect to the agent's workspace
    console.log(`Opening ${agentId}`);
  };

  const handleLogout = async () => {
    try {
      // Call logout API
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('authToken');
      // Call parent logout handler
      onLogout();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
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

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.first_name || 'Student'}! 👋
          </h1>
          <p className="text-gray-600">
            Choose an AI tutor to start your learning session or continue where you left off.
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
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
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Your AI Learning Partners</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {agents.map((agent) => {
              const colors = getColorClasses(agent.color);
              const IconComponent = agent.icon;
              
              return (
                <div
                  key={agent.id}
                  className={`bg-white rounded-xl shadow-sm border-2 ${colors.border} hover:shadow-md transition-all duration-200 cursor-pointer group ${colors.hover}`}
                  onClick={() => handleAgentClick(agent.id)}
                >
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className={`p-3 rounded-lg ${colors.bg}`}>
                        <IconComponent className={`h-8 w-8 ${colors.icon}`} />
                      </div>
                      <div className="flex items-center space-x-2">
                        <div className={`w-2 h-2 rounded-full ${
                          agent.status === 'online' ? 'bg-green-500' : 'bg-gray-400'
                        }`}></div>
                        <span className="text-xs text-gray-500 capitalize">{agent.status}</span>
                      </div>
                    </div>
                    
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{agent.name}</h3>
                    <p className="text-gray-600 mb-4">{agent.description}</p>
                    
                    <div className="space-y-2 mb-6">
                      {agent.features.map((feature, index) => (
                        <div key={index} className="flex items-center text-sm">
                          <div className={`w-1.5 h-1.5 rounded-full ${colors.icon} mr-2`}></div>
                          <span className="text-gray-600">{feature}</span>
                        </div>
                      ))}
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <button className={`px-4 py-2 rounded-lg ${colors.bg} ${colors.text} font-medium text-sm transition-colors group-hover:bg-opacity-80`}>
                        Start Session
                      </button>
                      <ArrowRightIcon className={`h-5 w-5 ${colors.icon} group-hover:translate-x-1 transition-transform`} />
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
                <AcademicCapIcon className="h-5 w-5 text-blue-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Completed Concept: Linear Algebra Basics</p>
                <p className="text-xs text-gray-500">2 hours ago with Concept Master</p>
              </div>
              <span className="text-xs text-green-600 font-medium">Completed</span>
            </div>
            
            <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
              <div className="p-2 bg-green-100 rounded-lg">
                <LightBulbIcon className="h-5 w-5 text-green-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Solved: Quadratic Equations</p>
                <p className="text-xs text-gray-500">4 hours ago with Problem Solver</p>
              </div>
              <span className="text-xs text-blue-600 font-medium">In Progress</span>
            </div>
            
            <div className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg">
              <div className="p-2 bg-purple-100 rounded-lg">
                <UserGroupIcon className="h-5 w-5 text-purple-600" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">Practice Quiz: Calculus Derivatives</p>
                <p className="text-xs text-gray-500">1 day ago with Practice Coach</p>
              </div>
              <span className="text-xs text-green-600 font-medium">Score: 85%</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
