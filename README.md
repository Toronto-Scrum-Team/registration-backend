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

### 1. Setup Environment

```bash
# Clone or navigate to the project directory
cd registration_backend

# Activate virtual environment (already created)
source venv/bin/activate

# Install dependencies (already installed)
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

1. **Change the SECRET_KEY** to a secure random value
2. **Set DEBUG=False** in environment variables
3. **Configure proper CORS origins** in `app/main.py`
4. **Use a production database** (PostgreSQL, MySQL) instead of SQLite
5. **Set up proper logging** and monitoring
6. **Use a production ASGI server** like Gunicorn with Uvicorn workers

## License

This project is open source and available under the MIT License.
