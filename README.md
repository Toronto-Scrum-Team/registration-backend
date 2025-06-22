# Registration Backend API

A secure user authentication backend with FastAPI, JWT tokens, and session management.

## Features

- User registration and authentication with JWT + session-based system
- Password security with bcrypt hashing
- Multi-device session management with automatic cleanup
- SQLite database with SQLAlchemy ORM (PostgreSQL ready)
- Comprehensive input validation and security features

## Technology Stack

- **FastAPI** with Uvicorn server
- **SQLite** with SQLAlchemy ORM
- **JWT + Session** authentication
- **bcrypt** password hashing
- **Pydantic** validation

## Prerequisites

- **Python 3.8+** and **pip**
- **Git** (recommended)

Tested on macOS, Linux, and Windows.

## Project Structure

```text
registration_backend/
├── .github/                # Github CI pipeline
│   └── workflows/          # Github actions workflows default folder
│       └── ci.yml          # CI script
├── app/                    # Main application code
│   ├── main.py             # FastAPI entry point
│   ├── models/             # Database models (User, Session)
│   ├── routes/             # API endpoints (auth, session)
│   ├── schemas/            # Pydantic validation schemas
│   └── utils/              # Authentication & session utilities
├── tests/                  # Testcases
├── frontend_session_integration/  # Frontend integration files
├── requirements.txt        # Dependencies
├── .env.template          # Environment configuration template
├── run.py                 # Application runner
└── README.md              # This file
```

## Quick Start

> **Note**: Make sure you have met all the [Prerequisites](#prerequisites) before proceeding.

### 1. Setup Environment

```bash
# Clone or navigate to the project directory
cd registration_backend

# Create virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment template and modify as needed:

```bash
cp .env.template .env
```

Edit `.env` file with your configuration:

- `SECRET_KEY`: Change to a secure random key for production
- `DATABASE_URL`: SQLite database path (default: `sqlite:///./registration.db`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time (default: 30 minutes)
- `SESSION_EXPIRE_HOURS`: Session expiration time (default: 168 hours / 7 days)
- `SESSION_CLEANUP_INTERVAL_HOURS`: Automatic cleanup interval (default: 24 hours)

### 3. Run the Application

```bash
# Using the runner script
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

The application will start on `http://localhost:8080`

### 4. Access API Documentation

Visit `http://localhost:8080/docs` for interactive API documentation with all endpoints and schemas.

## API Overview

The API provides the following main endpoints:

- **Authentication**: `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`
- **Session Management**: `/sessions/`, `/sessions/terminate`, `/sessions/terminate-all`
- **Utility**: `/`, `/health`

For detailed request/response schemas and testing, use the interactive documentation at `/docs`.

## Testing the API

The easiest way to test the API is through the interactive documentation at `http://localhost:8080/docs`.

You can also use curl or any HTTP client. Basic workflow:
1. Register a user at `/auth/register`
2. Login at `/auth/login` to get a JWT token
3. Use the token in the `Authorization: Bearer <token>` header for protected endpoints
4. Manage sessions through `/sessions/` endpoints

## Security Features

- **Password Security**: bcrypt hashing with strength requirements
- **JWT + Session Authentication**: Hybrid authentication system
- **UUID Identifiers**: Secure, unpredictable IDs for all records
- **Input Validation**: Comprehensive Pydantic validation
- **Session Management**: Multi-device support with automatic cleanup
- **SQL Injection Protection**: SQLAlchemy ORM security

## Configuration

Key environment variables (see `.env.template`):

- `SECRET_KEY`: JWT signing key (change for production)
- `DATABASE_URL`: Database connection string
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token lifetime (default: 30)
- `SESSION_EXPIRE_HOURS`: Session lifetime (default: 168 hours/7 days)
- `SESSION_CLEANUP_INTERVAL_HOURS`: Cleanup frequency (default: 24)

## Frontend Integration

The `frontend_session_integration/` folder contains React/Next.js integration files with session management UI components.

To integrate:
1. Copy files from `frontend_session_integration/src/` to your frontend project
2. Install dependencies and start development
3. See `frontend_session_integration/INTEGRATION_GUIDE.md` for details

## Production Deployment

For production:
- Change `SECRET_KEY` to a secure random value
- Set `DEBUG=False`
- Use PostgreSQL/MySQL instead of SQLite
- Configure proper CORS origins
- Use Gunicorn with Uvicorn workers
- Set up SSL/TLS for HTTPS

