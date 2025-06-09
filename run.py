#!/usr/bin/env python3
"""
Application runner for the Registration Backend API.
"""

import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=settings.DEBUG,
        log_level="info"
    )
