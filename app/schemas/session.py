from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    device_info: Optional[str] = Field(None, description="Device/browser information")

class SessionCreate(SessionBase):
    expires_at: datetime = Field(..., description="Session expiration timestamp")

class SessionResponse(BaseModel):
    session_id: str = Field(..., description="Session ID as string")
    user_id: str = Field(..., description="User ID as string")
    expires_at: str = Field(..., description="Session expiration timestamp in ISO format")
    device_info: Optional[str] = Field(None, description="Device/browser information")
    created_at: str = Field(..., description="Session creation timestamp in ISO format")
    last_accessed_at: Optional[str] = Field(None, description="Last access timestamp in ISO format")

    class Config:
        from_attributes = True

class SessionListResponse(BaseModel):
    sessions: list[SessionResponse] = Field(..., description="List of active sessions")
    total: int = Field(..., description="Total number of active sessions")

class SessionTerminateRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to terminate")

class SessionTerminateResponse(BaseModel):
    message: str = Field(..., description="Termination success message")
    success: bool = Field(default=True, description="Termination operation success status")

class SessionCleanupResponse(BaseModel):
    message: str = Field(..., description="Cleanup success message")
    cleaned_sessions: int = Field(..., description="Number of expired sessions cleaned up")
    success: bool = Field(default=True, description="Cleanup operation success status")
