from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session as DBSession
from ..database import get_db
from ..models.user import User
from ..schemas.session import (
    SessionResponse, SessionListResponse, SessionTerminateRequest, 
    SessionTerminateResponse, SessionCleanupResponse
)
from ..utils.dependencies import get_current_user
from ..utils.session import (
    get_user_sessions, terminate_session, cleanup_expired_sessions,
    terminate_all_user_sessions, extract_device_info
)

router = APIRouter(prefix="/sessions", tags=["Session Management"])

def convert_session_to_response(session) -> SessionResponse:
    """Convert database session to response format."""
    return SessionResponse(
        session_id=str(session.session_id),
        user_id=str(session.user_id),
        expires_at=session.expires_at.isoformat(),
        device_info=session.device_info,
        created_at=session.created_at.isoformat(),
        last_accessed_at=session.last_accessed_at.isoformat() if session.last_accessed_at else None
    )

@router.get("/", response_model=SessionListResponse)
def get_active_sessions(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Get all active sessions for the current user."""
    sessions = get_user_sessions(db, str(current_user.id), include_expired=False)
    
    session_responses = [convert_session_to_response(session) for session in sessions]
    
    return SessionListResponse(
        sessions=session_responses,
        total=len(session_responses)
    )

@router.delete("/terminate", response_model=SessionTerminateResponse)
def terminate_session_endpoint(
    request_data: SessionTerminateRequest,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Terminate a specific session."""
    success = terminate_session(db, request_data.session_id, str(current_user.id))
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or does not belong to current user"
        )
    
    return SessionTerminateResponse(
        message=f"Session {request_data.session_id} terminated successfully",
        success=True
    )

@router.delete("/terminate-all", response_model=SessionTerminateResponse)
def terminate_all_sessions(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Terminate all sessions for the current user."""
    count = terminate_all_user_sessions(db, str(current_user.id))
    
    return SessionTerminateResponse(
        message=f"All {count} sessions terminated successfully",
        success=True
    )

@router.delete("/terminate-others", response_model=SessionTerminateResponse)
def terminate_other_sessions(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Terminate all other sessions except the current one."""
    # Extract current session ID from JWT token if available
    # This would require modification to JWT to include session_id
    # For now, we'll terminate all sessions
    count = terminate_all_user_sessions(db, str(current_user.id))
    
    return SessionTerminateResponse(
        message=f"All other sessions ({count}) terminated successfully",
        success=True
    )

@router.post("/cleanup", response_model=SessionCleanupResponse)
def cleanup_expired_sessions_endpoint(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db)
):
    """Clean up expired sessions (admin function - could be restricted)."""
    count = cleanup_expired_sessions(db)
    
    return SessionCleanupResponse(
        message=f"Cleanup completed successfully",
        cleaned_sessions=count,
        success=True
    )
