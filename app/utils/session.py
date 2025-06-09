from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session as DBSession
from ..models.session import Session
from ..models.user import User
from ..config import settings
import uuid
import json

def create_session(
    db: DBSession,
    user: User,
    device_info: Optional[str] = None,
    expires_delta: Optional[timedelta] = None
) -> Session:
    """Create a new session for a user."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default session expiration (longer than JWT for persistent sessions)
        expire = datetime.now(timezone.utc) + timedelta(hours=24 * 7)  # 7 days

    # Store as timezone-naive datetime for SQLite compatibility
    expire_naive = expire.replace(tzinfo=None)

    session = Session(
        user_id=user.id,
        expires_at=expire_naive,
        device_info=device_info
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

def get_session_by_id(db: DBSession, session_id: str) -> Optional[Session]:
    """Get a session by its ID."""
    try:
        session_uuid = uuid.UUID(session_id)
        return db.query(Session).filter(Session.session_id == session_uuid).first()
    except ValueError:
        return None

def validate_session(db: DBSession, session_id: str) -> Optional[Session]:
    """Validate a session and return it if valid."""
    session = get_session_by_id(db, session_id)
    
    if not session:
        return None
    
    if session.is_expired():
        # Clean up expired session
        db.delete(session)
        db.commit()
        return None
    
    # Update last accessed time
    session.update_last_accessed()
    db.commit()
    
    return session

def terminate_session(db: DBSession, session_id: str, user_id: Optional[str] = None) -> bool:
    """Terminate a session. If user_id is provided, only terminate if it belongs to that user."""
    session = get_session_by_id(db, session_id)
    
    if not session:
        return False
    
    # If user_id is provided, ensure the session belongs to that user
    if user_id and str(session.user_id) != user_id:
        return False
    
    db.delete(session)
    db.commit()
    return True

def get_user_sessions(db: DBSession, user_id: str, include_expired: bool = False) -> list[Session]:
    """Get all sessions for a user."""
    try:
        user_uuid = uuid.UUID(user_id)
        query = db.query(Session).filter(Session.user_id == user_uuid)

        if not include_expired:
            # Use timezone-naive datetime for SQLite compatibility
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            query = query.filter(Session.expires_at > now)

        return query.order_by(Session.created_at.desc()).all()
    except ValueError:
        return []

def cleanup_expired_sessions(db: DBSession) -> int:
    """Clean up all expired sessions and return the count of cleaned sessions."""
    # Use timezone-naive datetime for SQLite compatibility
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expired_sessions = db.query(Session).filter(
        Session.expires_at <= now
    ).all()

    count = len(expired_sessions)

    for session in expired_sessions:
        db.delete(session)

    db.commit()
    return count

def terminate_all_user_sessions(db: DBSession, user_id: str, except_session_id: Optional[str] = None) -> int:
    """Terminate all sessions for a user, optionally except one session."""
    try:
        user_uuid = uuid.UUID(user_id)
        query = db.query(Session).filter(Session.user_id == user_uuid)
        
        if except_session_id:
            except_uuid = uuid.UUID(except_session_id)
            query = query.filter(Session.session_id != except_uuid)
        
        sessions = query.all()
        count = len(sessions)
        
        for session in sessions:
            db.delete(session)
        
        db.commit()
        return count
    except ValueError:
        return 0

def extract_device_info(user_agent: Optional[str] = None, ip_address: Optional[str] = None) -> str:
    """Extract and format device information from request headers."""
    device_info = {}
    
    if user_agent:
        device_info["user_agent"] = user_agent
    
    if ip_address:
        device_info["ip_address"] = ip_address
    
    device_info["timestamp"] = datetime.now(timezone.utc).isoformat()
    
    return json.dumps(device_info)
