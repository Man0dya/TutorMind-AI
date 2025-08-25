import { useState } from 'react';
import { 
  DocumentTextIcon, 
  AcademicCapIcon, 
  LightBulbIcon, 
  BookOpenIcon,
  SparklesIcon,
  CheckIcon
} from '@heroicons/react/24/outline';

const ContentGeneratorForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    difficultyLevel: '',
    contentType: '',
    customTopic: ''
  });
  const [errors, setErrors] = useState({});
  const [showCustomTopic, setShowCustomTopic] = useState(false);

  // Predefined topics for easy selection
  const predefinedTopics = [
    'Linear Algebra',
    'Calculus',
    'Statistics',
    'Physics',
    'Chemistry',
    'Biology',
    'Computer Science',
    'Economics',
    'Psychology',
    'History',
    'Literature',
    'Philosophy'
  ];

  // Difficulty levels
  const difficultyLevels = [
    { value: 'beginner', label: 'Beginner', description: 'Basic concepts and fundamentals' },
    { value: 'intermediate', label: 'Intermediate', description: 'Moderate complexity with examples' },
    { value: 'advanced', label: 'Advanced', description: 'Complex topics with deep analysis' }
  ];

  // Content types
  const contentTypes = [
    { value: 'study-notes', label: 'Study Notes', description: 'Concise notes for revision' },
    { value: 'explanation', label: 'Explanation', description: 'Detailed explanations with examples' },
    { value: 'summary', label: 'Summary', description: 'Key points and overview' },
    { value: 'tutorial', label: 'Tutorial', description: 'Step-by-step learning guide' },
    { value: 'cheat-sheet', label: 'Cheat Sheet', description: 'Quick reference guide' },
    { value: 'mind-map', label: 'Mind Map', description: 'Visual concept organization' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear errors when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }

    // Handle topic selection
    if (name === 'topic') {
      if (value === 'custom') {
        setShowCustomTopic(true);
        setFormData(prev => ({ ...prev, customTopic: '' }));
      } else {
        setShowCustomTopic(false);
        setFormData(prev => ({ ...prev, customTopic: value }));
      }
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.topic && !formData.customTopic) {
      newErrors.topic = 'Please select or enter a topic';
    }
    
    if (formData.topic === 'custom' && !formData.customTopic.trim()) {
      newErrors.customTopic = 'Please enter a custom topic';
    }
    
    if (!formData.difficultyLevel) {
      newErrors.difficultyLevel = 'Please select a difficulty level';
    }
    
    if (!formData.contentType) {
      newErrors.contentType = 'Please select a content type';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const submissionData = {
      topic: formData.topic === 'custom' ? formData.customTopic : formData.topic,
      difficultyLevel: formData.difficultyLevel,
      contentType: formData.contentType,
      timestamp: new Date().toISOString()
    };

    onSubmit(submissionData);
  };

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'beginner': return 'text-green-600 bg-green-50 border-green-200';
      case 'intermediate': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'advanced': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getContentTypeIcon = (type) => {
    switch (type) {
      case 'study-notes': return BookOpenIcon;
      case 'explanation': return LightBulbIcon;
      case 'summary': return DocumentTextIcon;
      case 'tutorial': return AcademicCapIcon;
      case 'cheat-sheet': return SparklesIcon;
      case 'mind-map': return AcademicCapIcon;
      default: return DocumentTextIcon;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Generate Learning Content</h2>
        <p className="text-gray-600">
          Fill in the details below to generate personalized learning content tailored to your needs.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Topic Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Learning Topic *
          </label>
          
          {/* Predefined Topics */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
            {predefinedTopics.map((topic) => (
              <button
                key={topic}
                type="button"
                onClick={() => {
                  setFormData(prev => ({ 
                    ...prev, 
                    topic: topic,
                    customTopic: topic 
                  }));
                  setShowCustomTopic(false);
                }}
                className={`p-3 text-sm font-medium rounded-lg border-2 transition-all ${
                  formData.topic === topic
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                {topic}
              </button>
            ))}
            
            {/* Custom Topic Option */}
            <button
              type="button"
              onClick={() => {
                setFormData(prev => ({ ...prev, topic: 'custom' }));
                setShowCustomTopic(true);
              }}
              className={`p-3 text-sm font-medium rounded-lg border-2 transition-all ${
                formData.topic === 'custom'
                  ? 'border-blue-500 bg-blue-50 text-blue-700'
                  : 'border-gray-200 bg-white text-gray-700 hover:border-gray-300 hover:bg-gray-50'
              }`}
            >
              + Custom Topic
            </button>
          </div>

          {/* Custom Topic Input */}
          {showCustomTopic && (
            <div className="mt-4">
              <input
                type="text"
                name="customTopic"
                value={formData.customTopic}
                onChange={handleChange}
                placeholder="Enter your custom topic..."
                className={`w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
                  errors.customTopic ? 'border-red-300' : 'border-gray-300'
                }`}
              />
              {errors.customTopic && (
                <p className="mt-1 text-sm text-red-600">{errors.customTopic}</p>
              )}
            </div>
          )}

          {errors.topic && (
            <p className="mt-1 text-sm text-red-600">{errors.topic}</p>
          )}
        </div>

        {/* Difficulty Level */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Difficulty Level *
          </label>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {difficultyLevels.map((level) => (
              <button
                key={level.value}
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, difficultyLevel: level.value }))}
                className={`p-4 text-left rounded-lg border-2 transition-all ${
                  formData.difficultyLevel === level.value
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className={`text-sm font-medium ${
                    formData.difficultyLevel === level.value ? 'text-blue-700' : 'text-gray-700'
                  }`}>
                    {level.label}
                  </span>
                  {formData.difficultyLevel === level.value && (
                    <CheckIcon className="h-5 w-5 text-blue-600" />
                  )}
                </div>
                <p className={`text-xs ${
                  formData.difficultyLevel === level.value ? 'text-blue-600' : 'text-gray-500'
                }`}>
                  {level.description}
                </p>
              </button>
            ))}
          </div>
          {errors.difficultyLevel && (
            <p className="mt-1 text-sm text-red-600">{errors.difficultyLevel}</p>
          )}
        </div>

        {/* Content Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Content Type *
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {contentTypes.map((type) => {
              const IconComponent = getContentTypeIcon(type.value);
              return (
                <button
                  key={type.value}
                  type="button"
                  onClick={() => setFormData(prev => ({ ...prev, contentType: type.value }))}
                  className={`p-4 text-left rounded-lg border-2 transition-all ${
                    formData.contentType === type.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-3">
                      <IconComponent className={`h-5 w-5 ${
                        formData.contentType === type.value ? 'text-blue-600' : 'text-gray-400'
                      }`} />
                      <span className={`text-sm font-medium ${
                        formData.contentType === type.value ? 'text-blue-700' : 'text-gray-700'
                      }`}>
                        {type.label}
                      </span>
                    </div>
                    {formData.contentType === type.value && (
                      <CheckIcon className="h-5 w-5 text-blue-600" />
                    )}
                  </div>
                  <p className={`text-xs ${
                    formData.contentType === type.value ? 'text-blue-600' : 'text-gray-500'
                  }`}>
                    {type.description}
                  </p>
                </button>
              );
            })}
          </div>
          {errors.contentType && (
            <p className="mt-1 text-sm text-red-600">{errors.contentType}</p>
          )}
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center items-center px-6 py-4 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
                Generating Content...
              </>
            ) : (
              <>
                <SparklesIcon className="h-5 w-5 mr-2" />
                Generate Content
              </>
            )}
          </button>
        </div>
      </form>

      {/* Form Summary */}
      {formData.topic && formData.difficultyLevel && formData.contentType && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Content Summary</h3>
          <div className="text-sm text-gray-600 space-y-1">
            <p><span className="font-medium">Topic:</span> {formData.topic === 'custom' ? formData.customTopic : formData.topic}</p>
            <p><span className="font-medium">Difficulty:</span> {difficultyLevels.find(l => l.value === formData.difficultyLevel)?.label}</p>
            <p><span className="font-medium">Type:</span> {contentTypes.find(t => t.value === formData.contentType)?.label}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentGeneratorForm;
