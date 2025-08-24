# TutorMind AI Backend

FastAPI backend for the multi-agent AI tutoring system with MongoDB integration and JWT authentication.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ installed
- MongoDB running locally or accessible via connection string
- pip package manager

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the backend directory with:
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

### 3. Start MongoDB
Make sure MongoDB is running on your system.

### 4. Run the Server
```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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

## 🔐 Authentication

The API uses JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## 🗄️ Database

MongoDB collections:
- `users` - User accounts and authentication data

## 🛠️ Development

The backend is structured with:
- `app/models/` - Pydantic models for data validation
- `app/routes/` - API route handlers
- `app/services/` - Business logic
- `app/utils/` - Utility functions (database, security)
- `app/config.py` - Configuration settings
