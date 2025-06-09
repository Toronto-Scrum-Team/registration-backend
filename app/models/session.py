from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..database import Base
from .user import GUID

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    device_info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship to User model
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id}, expires_at={self.expires_at})>"

    def is_expired(self) -> bool:
        """Check if the session is expired."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)

        # Handle timezone-naive datetime from SQLite
        if self.expires_at.tzinfo is None:
            # Convert to UTC for comparison
            expires_at_utc = self.expires_at.replace(tzinfo=timezone.utc)
        else:
            expires_at_utc = self.expires_at

        return now > expires_at_utc

    def update_last_accessed(self):
        """Update the last accessed timestamp."""
        from datetime import datetime, timezone
        self.last_accessed_at = datetime.now(timezone.utc)
