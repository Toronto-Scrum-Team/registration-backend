from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token, LogoutResponse
from ..utils.auth import get_password_hash, verify_password, create_access_token, create_access_token_with_session
from ..utils.dependencies import get_current_user
from ..utils.session import create_session, extract_device_info, terminate_all_user_sessions
import re

router = APIRouter(prefix="/auth", tags=["Authentication"])

def validate_password_strength(password: str) -> bool:
    """Validate password meets frontend requirements."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False
    return True

def convert_user_to_response(user: User) -> UserResponse:
    """Convert database user to frontend-compatible response."""
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        createdAt=user.created_at.isoformat()
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""

    # Validate password confirmation
    if user_data.password != user_data.confirmPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Validate password strength
    if not validate_password_strength(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters and contain at least one uppercase letter, one number and one special character"
        )

    # Check if email already exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create full name from first and last name
    full_name = f"{user_data.firstName} {user_data.lastName}".strip()

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        name=full_name,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return convert_user_to_response(db_user)

@router.post("/login", response_model=Token)
def login_user(user_credentials: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Authenticate user and return access token with session."""

    # Find user by email
    user = db.query(User).filter(User.email == user_credentials.email).first()

    # Verify user exists and password is correct
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract device information
    user_agent = request.headers.get("user-agent")
    # Get client IP (considering proxy headers)
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else None)
    device_info = extract_device_info(user_agent, client_ip)

    # Create session
    session = create_session(db, user, device_info)

    # Create access token with session information
    access_token = create_access_token_with_session(
        data={"sub": user.email},
        session_id=str(session.session_id)
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return convert_user_to_response(current_user)

@router.post("/logout", response_model=LogoutResponse)
def logout_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout the current authenticated user and terminate all sessions.

    This endpoint validates the JWT token, terminates all user sessions,
    and returns a success response.
    """
    # Terminate all sessions for the user
    terminated_count = terminate_all_user_sessions(db, str(current_user.id))

    return LogoutResponse(
        message=f"User {current_user.email} logged out successfully. {terminated_count} sessions terminated.",
        success=True
    )

