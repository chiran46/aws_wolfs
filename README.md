# CarbonSakthi AI Backend

A comprehensive FastAPI backend for CarbonSakthi AI platform - Sustainable farming and carbon credit management system.

## Features

- **Farmer Management**: Register, update, and manage farmer profiles
- **Carbon Credits**: Track and manage carbon sequestration credits
- **Farm Activities**: Log and monitor farming activities with carbon impact
- **Authentication & Authorization**: JWT-based secure authentication system
- **Database Integration**: SQLAlchemy ORM with SQLite (easily configurable for PostgreSQL/MySQL)
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Error Handling**: Comprehensive exception handling and logging
- **CORS Support**: Cross-origin resource sharing configuration

## Project Structure

```
carbonsakthi-backend/
├── main.py                 # FastAPI application entry point
├── config/
│   ├── settings.py         # Application settings and environment variables
│   └── database.py         # Database configuration and session management
├── models/
│   ├── farmer.py           # Farmer, CarbonCredit, FarmActivity models
│   └── auth.py             # User authentication model
├── routes/
│   ├── farmer.py           # Farmer-related API endpoints
│   └── auth.py             # Authentication endpoints
├── services/
│   ├── farmer_service.py   # Farmer business logic
│   └── auth_service.py     # Authentication business logic
├── utils/
│   ├── logger.py           # Logging configuration
│   └── exceptions.py       # Custom exception classes
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd carbonsakthi-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env` file and update with your settings
   - At minimum, update the `SECRET_KEY` for production

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info
- `GET /api/v1/auth/verify-token` - Verify token validity

### Farmers
- `POST /api/v1/farmer/register` - Register new farmer
- `GET /api/v1/farmer/{farmer_id}` - Get farmer by ID
- `GET /api/v1/farmers` - Get all farmers (with pagination)
- `PUT /api/v1/farmer/{farmer_id}` - Update farmer information
- `DELETE /api/v1/farmer/{farmer_id}` - Soft delete farmer
- `GET /api/v1/farmers/location/{location}` - Get farmers by location
- `GET /api/v1/farmers/crop/{crop_type}` - Get farmers by crop type

### Carbon Credits
- `POST /api/v1/farmer/{farmer_id}/carbon-credit` - Create carbon credit
- `GET /api/v1/farmer/{farmer_id}/carbon-credits` - Get farmer's carbon credits

### Farm Activities
- `POST /api/v1/farmer/{farmer_id}/activity` - Create farm activity
- `GET /api/v1/farmer/{farmer_id}/activities` - Get farmer's activities

### System
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint

## Environment Variables

Key environment variables in `.env`:

```env
# Application
APP_NAME="CarbonSakthi AI"
DEBUG=True

# Database
DATABASE_URL="sqlite:///./carbonsakthi.db"

# Security
SECRET_KEY="your-secret-key-here-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# AWS (for future use)
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_REGION="us-east-1"

# External APIs
WEATHER_API_KEY=""
CARBON_API_KEY=""
```

## Database Setup

### SQLite (Default)
The application uses SQLite by default with the database file `carbonsakthi.db` created automatically.

### PostgreSQL
To use PostgreSQL instead:

1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```

2. Update `.env`:
   ```env
   DATABASE_URL="postgresql://username:password@localhost/carbonsakthi_db"
   ```

### MySQL
To use MySQL:

1. Install MySQL driver:
   ```bash
   pip install PyMySQL
   ```

2. Update `.env`:
   ```env
   DATABASE_URL="mysql+pymysql://username:password@localhost/carbonsakthi_db"
   ```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register a user or login to get an access token
2. Include the token in the Authorization header:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes and descriptive error messages.

## Logging

Application logs are written to both:
- Console output
- Log file: `carbonsakthi.log`

Log level can be configured via `LOG_LEVEL` environment variable.

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --log-level debug
```

### Database Migrations
For production deployments, consider using Alembic for database migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Production Deployment

For production deployment:

1. Use a production-grade WSGI server (Gunicorn, Uvicorn with workers)
2. Use PostgreSQL or MySQL instead of SQLite
3. Set up proper environment variables
4. Configure reverse proxy (Nginx)
5. Set up SSL/TLS
6. Monitor logs and application health

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
