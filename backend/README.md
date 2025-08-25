# TutorMind AI Backend

FastAPI backend for the multi-agent AI tutoring system with MongoDB Atlas integration and JWT authentication.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+ installed
- MongoDB Atlas cluster accessible
- pip package manager

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the backend directory with your MongoDB Atlas credentials:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://AI:IbxZrJMQZntmtBoF@cluster0.uvtm7dl.mongodb.net/
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

**⚠️ Important:** 
- Copy the `.env` file from `env.example` and update with your actual MongoDB Atlas credentials
- Never commit your `.env` file to version control
- Keep your MongoDB Atlas credentials secure

### 3. Test MongoDB Atlas Connection
Before starting the server, test your database connection:

```bash
python test_connection.py
```

This will verify:
- ✅ MongoDB Atlas connectivity
- ✅ Authentication credentials
- ✅ Database access permissions

### 4. Start the Server
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

MongoDB Atlas collections:
- `users` - User accounts and authentication data

### Database Schema
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

The backend is structured with:
- `app/models/` - Pydantic models for data validation
- `app/routes/` - API route handlers
- `app/services/` - Business logic
- `app/utils/` - Utility functions (database, security)
- `app/config.py` - Configuration settings

## 🔧 Troubleshooting

### Connection Issues
1. **Test connection first:** `python test_connection.py`
2. **Check MongoDB Atlas:**
   - Network access (IP whitelist)
   - Database user permissions
   - Connection string format
3. **Verify environment variables** in `.env` file

### Common Errors
- `ServerSelectionTimeoutError`: Network connectivity issue
- `AuthenticationFailed`: Invalid username/password
- `OperationFailure`: Insufficient permissions

## 📊 Monitoring

The backend includes comprehensive logging:
- ✅ Connection status
- ✅ User operations (create, login, update)
- ✅ JWT token operations
- ❌ Error details with context

## 🚀 Production Notes

- Change `JWT_SECRET_KEY` to a secure random string
- Set `DEBUG=False` in production
- Configure proper CORS origins
- Use environment-specific MongoDB Atlas clusters
- Implement rate limiting and security headers
