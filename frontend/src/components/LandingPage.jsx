import { Link } from 'react-router-dom';
import { AcademicCapIcon, LightBulbIcon, UserGroupIcon, RocketLaunchIcon } from '@heroicons/react/24/outline';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <AcademicCapIcon className="h-8 w-8 text-blue-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">TutorMind AI</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/login"
                className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Revolutionize Learning with
            <span className="text-blue-600 block">Multi-Agent AI Tutors</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Experience personalized education powered by three specialized AI agents: 
            Concept Master, Problem Solver, and Practice Coach. 
            Learn smarter, faster, and more effectively.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/signup"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-lg font-semibold transition-colors shadow-lg hover:shadow-xl"
            >
              Start Learning Free
            </Link>
            <Link
              to="/login"
              className="border-2 border-gray-300 hover:border-gray-400 text-gray-700 hover:text-gray-900 px-8 py-4 rounded-lg text-lg font-semibold transition-colors"
            >
              Sign In
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Meet Your AI Learning Partners
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Each agent specializes in different aspects of learning to provide comprehensive support
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {/* Concept Master */}
          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <AcademicCapIcon className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Concept Master</h3>
            <p className="text-gray-600 mb-6">
              Breaks down complex topics into simple, digestible concepts. 
              Explains theories, provides examples, and ensures fundamental understanding.
            </p>
            <div className="text-sm text-blue-600 font-medium">• Theory & Concepts</div>
            <div className="text-sm text-blue-600 font-medium">• Examples & Analogies</div>
            <div className="text-sm text-blue-600 font-medium">• Fundamental Building Blocks</div>
          </div>

          {/* Problem Solver */}
          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <LightBulbIcon className="h-8 w-8 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Problem Solver</h3>
            <p className="text-gray-600 mb-6">
              Guides you through step-by-step problem solutions. 
              Teaches problem-solving strategies and critical thinking skills.
            </p>
            <div className="text-sm text-green-600 font-medium">• Step-by-step Solutions</div>
            <div className="text-sm text-green-600 font-medium">• Problem Strategies</div>
            <div className="text-sm text-green-600 font-medium">• Critical Thinking</div>
          </div>

          {/* Practice Coach */}
          <div className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-100">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <UserGroupIcon className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Practice Coach</h3>
            <p className="text-gray-600 mb-6">
              Creates personalized practice exercises and quizzes. 
              Tracks progress and adapts difficulty to your learning pace.
            </p>
            <div className="text-sm text-purple-600 font-medium">• Custom Exercises</div>
            <div className="text-sm text-purple-600 font-medium">• Progress Tracking</div>
            <div className="text-sm text-purple-600 font-medium">• Adaptive Learning</div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 py-20">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Learning Experience?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of students already learning smarter with AI-powered tutoring
          </p>
          <Link
            to="/signup"
            className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-4 rounded-lg text-lg font-semibold transition-colors shadow-lg hover:shadow-xl inline-block"
          >
            <RocketLaunchIcon className="h-5 w-5 inline mr-2" />
            Get Started Now
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-6">
              <AcademicCapIcon className="h-8 w-8 text-blue-400" />
              <span className="ml-2 text-xl font-bold">TutorMind AI</span>
            </div>
            <p className="text-gray-400 mb-4">
              Empowering students with intelligent, personalized learning experiences
            </p>
            <div className="text-sm text-gray-500">
              © 2024 TutorMind AI. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
