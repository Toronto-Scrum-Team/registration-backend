from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.session import Session as UserSession
from .auth import verify_token, verify_token_with_session
from .session import validate_session

# Security scheme for JWT
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token
    email = verify_token(credentials.credentials)
    if email is None:
        raise credentials_exception

    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

def get_current_user_with_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> tuple[User, UserSession]:
    """Get the current authenticated user and validate their session."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token and extract session info
    token_data = verify_token_with_session(credentials.credentials)
    if token_data is None:
        raise credentials_exception

    email, session_id = token_data

    # Get user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    # If session_id is present, validate the session
    if session_id:
        session = validate_session(db, session_id)
        if session is None or str(session.user_id) != str(user.id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user, session
    else:
        # For backward compatibility with tokens without session_id
        # Create a temporary session object or handle as needed
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session information required",
            headers={"WWW-Authenticate": "Bearer"},
        )
