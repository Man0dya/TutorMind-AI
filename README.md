# TutorMind AI - Multi-Agent AI Tutoring System

A comprehensive AI-powered tutoring system featuring three specialized AI agents: Concept Master, Problem Solver, and Practice Coach.

## 🚀 Features

- **Multi-Agent AI System**: Three specialized AI tutors for different learning aspects
- **Modern React Frontend**: Built with React, Tailwind CSS, and Vite
- **FastAPI Backend**: Python backend with MongoDB integration
- **JWT Authentication**: Secure user authentication and session management
- **Responsive Design**: Mobile-first design that works on all devices

## 🏗️ Architecture

```
TutorMind-AI/
├── frontend/          # React frontend application
├── backend/           # FastAPI Python backend
└── README.md         # This file
```

## 🎯 AI Agents

1. **Concept Master** (Blue) - Theory & concepts, examples, fundamental building blocks
2. **Problem Solver** (Green) - Step-by-step solutions, problem strategies, critical thinking
3. **Practice Coach** (Purple) - Custom exercises, progress tracking, adaptive learning

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- MongoDB running locally or accessible
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd TutorMind-AI
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` or `http://localhost:5174`

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=tutormind

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRES_MINUTES=1440

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

Start the backend:
```bash
python run.py
```

The backend will be available at `http://localhost:8000`

### 4. Frontend Environment
Create a `.env.local` file in the frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=TutorMind AI
```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info (protected)
- `POST /auth/logout` - User logout

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check

## 🔐 Authentication Flow

1. User registers/logs in through the frontend
2. Backend validates credentials and returns JWT token
3. Frontend stores token in localStorage
4. Token is included in subsequent API requests
5. Backend validates token for protected endpoints

## 🗄️ Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "hashed_password": "bcrypt_hash",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_active": true,
  "avatar": null
}
```

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
cd backend
python run.py        # Start with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database
Make sure MongoDB is running:
```bash
# Start MongoDB (if installed locally)
mongod

# Or use Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

## 🔧 Configuration

### Frontend Configuration
- Environment variables in `.env.local`
- Tailwind CSS configuration in `tailwind.config.js`
- Vite configuration in `vite.config.js`

### Backend Configuration
- Environment variables in `.env`
- CORS origins in `app/config.py`
- Database connection in `app/utils/database.py`

## 📱 User Experience

1. **Landing Page**: Beautiful homepage with feature showcase
2. **Authentication**: Secure signup/login with validation
3. **Dashboard**: Overview of AI agents and learning progress
4. **AI Agents**: Interactive cards for each specialized tutor
5. **Responsive Design**: Works seamlessly on all devices

## 🚀 Next Steps

- [ ] Implement AI agent chat interfaces
- [ ] Add Gemini API integration for AI responses
- [ ] Create learning session management
- [ ] Add progress tracking and analytics
- [ ] Implement real-time notifications
- [ ] Add admin dashboard for user management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in each directory
- Review the API endpoints at `/docs` when backend is running

---

**TutorMind AI** - Revolutionizing education with multi-agent AI tutoring! 🎓✨
