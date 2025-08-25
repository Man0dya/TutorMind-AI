from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserCreate, UserLogin, UserResponse, Token
from app.services.user_service import UserService
from app.utils.security import verify_token
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_service = UserService()
    user = await user_service.get_user_by_id(payload.get("sub"))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user."""
    try:
        logger.info(f"🔄 Attempting to register user: {user.email}")
        user_service = UserService()
        new_user = await user_service.create_user(user)
        logger.info(f"✅ User created successfully: {new_user.email}")
        
        # Create access token
        access_token = user_service.create_user_token(new_user)
        logger.info(f"🔑 JWT token created for user: {new_user.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=new_user
        )
    except ValueError as e:
        logger.warning(f"❌ Validation error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"💥 Unexpected error during registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Authenticate user and return JWT token."""
    try:
        logger.info(f"🔐 Attempting login for user: {user_credentials.email}")
        user_service = UserService()
        user = await user_service.authenticate_user(
            user_credentials.email, 
            user_credentials.password
        )
        
        if not user:
            logger.warning(f"❌ Login failed for user: {user_credentials.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = user_service.create_user_token(user)
        logger.info(f"✅ Login successful for user: {user.email}")
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"💥 Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.post("/logout")
async def logout():
    """Logout user (client should discard token)."""
    return {"message": "Successfully logged out"}
