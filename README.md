# Registration Backend API

The backend of user-registration build with FastAPI, SQLite, and JWT tokens.

## Features

- **User Registration**: Secure user registration with email and username validation
- **User Authentication**: JWT token-based authentication system
- **Password Security**: Bcrypt password hashing
- **Input Validation**: Comprehensive input validation using Pydantic
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Database**: SQLite database with SQLAlchemy ORM
- **CORS Support**: Cross-origin resource sharing enabled

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Validation**: Pydantic schemas
- **Server**: Uvicorn ASGI server

## Prerequisites

Before running this application, ensure you have the following installed on your system:

### System Requirements

- **Python 3.8 or higher** (Tested with Python 3.12.5)
  - Check your Python version: `python3 --version`
  - Download from: https://www.python.org/downloads/

- **pip** (Python package installer)
  - Usually comes with Python installation
  - Check if installed: `pip --version`

### Optional but Recommended

- **Git** (for version control)
  - Download from: https://git-scm.com/downloads
  - Check if installed: `git --version`

- **Virtual Environment Tools**
  - `venv` (included with Python 3.3+)
  - Or `virtualenv`: `pip install virtualenv`

### Operating System Support

This application has been tested on:
- **macOS** (Primary development environment)
- **Linux** (Ubuntu, CentOS, etc.)
- **Windows** (with Python 3.8+)

## Project Structure

```
registration_backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py          # Pydantic schemas for validation
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth.py          # Authentication routes
│   └── utils/
│       ├── __init__.py
│       ├── auth.py          # JWT and password utilities
│       └── dependencies.py  # FastAPI dependencies
├── venv/                    # Virtual environment
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── .env.template           # Environment template
├── .gitignore              # Git ignore rules
├── run.py                  # Application runner
└── README.md               # This file
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
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time

### 3. Run the Application

```bash
# Using the runner script
python run.py

# Or directly with uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8080
```

The application will start on `http://localhost:8080`

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## API Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-01T12:00:00Z"
}
```

#### POST /auth/login
Authenticate user and get access token.

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /auth/me
Get current authenticated user information (requires authentication).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-01T12:00:00Z"
}
```

### Utility Endpoints

#### GET /
Root endpoint with API information.

#### GET /health
Health check endpoint.

## Testing the API

### Using curl

1. **Register a new user:**
```bash
curl -X POST "http://localhost:8080/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpassword123"
     }'
```

2. **Login:**
```bash
curl -X POST "http://localhost:8080/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpassword123"
     }'
```

3. **Get user info (replace TOKEN with actual token):**
```bash
curl -X GET "http://localhost:8080/auth/me" \
     -H "Authorization: Bearer TOKEN"
```

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive validation of all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Configuration**: Configurable cross-origin resource sharing

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./registration.db` |
| `SECRET_KEY` | JWT signing secret key | Generated key |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `APP_NAME` | Application name | `Registration Backend` |
| `DEBUG` | Debug mode | `True` |

## Production Deployment

For production deployment:

1. **Ensure Python 3.8+** is installed on the production server
2. **Change the SECRET_KEY** to a secure random value
3. **Set DEBUG=False** in environment variables
4. **Configure proper CORS origins** in `app/main.py`
5. **Use a production database** (PostgreSQL, MySQL) instead of SQLite
6. **Set up proper logging** and monitoring
7. **Use a production ASGI server** like Gunicorn with Uvicorn workers
8. **Set up SSL/TLS** for HTTPS in production

## License

This project is open source and available under the MIT License.
