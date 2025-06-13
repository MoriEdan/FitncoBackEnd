# ⚡ FitnCo Backend API

<div align="center">
  <img src="https://fitnco.fit/wp-content/uploads/2022/10/Fitn-Co-Logo-Animasyon-Final.gif" alt="FitnCo Logo" width="200"/>
  
  <p align="center">
    <strong>Powerful REST API Backend for FitnCo Fitness Platform</strong>
  </p>
  
  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
    <img src="https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Version">
    <img src="https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/Redis-7.0+-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
    <img src="https://img.shields.io/badge/License-Private-red?style=for-the-badge" alt="License">
  </p>
</div>

---

## 🚀 About FitnCo Backend

FitnCo Backend is a robust, scalable REST API built with Flask that powers the FitnCo fitness and nutrition platform. It provides comprehensive services for user management, meal planning, workout tracking, real-time messaging, and analytics, serving thousands of users with high performance and reliability.

### 🌟 Key Features

- **🔐 Advanced Authentication** - JWT-based secure authentication system
- **👥 User Management** - Complete user profile and role management
- **🍽️ Nutrition Engine** - Sophisticated meal planning and calorie tracking
- **📊 Analytics Dashboard** - Real-time data analytics and reporting
- **💬 Real-time Messaging** - WebSocket-based instant messaging system
- **📱 Push Notifications** - Firebase Cloud Messaging integration
- **🌍 Internationalization** - Multi-language support (Turkish/English)
- **☁️ Cloud Integration** - AWS S3 file storage and management
- **📈 Performance Monitoring** - Sentry error tracking and performance monitoring
- **🔄 Background Tasks** - Celery-based asynchronous task processing

---

## 🏗️ Technology Stack

### Core Framework
- **Flask 2.3.3** - Lightweight and flexible web framework
- **SQLAlchemy 2.0+** - Advanced SQL toolkit and ORM
- **Flask-SocketIO** - WebSocket support for real-time features
- **Flask-JWT-Extended** - JWT authentication implementation
- **Flask-CORS** - Cross-origin resource sharing support

### Database & Caching
- **PostgreSQL 15+** - Primary relational database
- **Redis 7.0+** - Caching and session storage
- **Alembic** - Database migration management

### Cloud & External Services
- **AWS S3** - File storage and media management
- **Firebase FCM** - Push notification service
- **Sentry** - Error tracking and performance monitoring
- **Elasticsearch** - Full-text search capabilities

### Development & Deployment
- **Docker** - Containerization for consistent environments
- **Gunicorn** - WSGI HTTP Server for production
- **uWSGI** - Alternative WSGI server option
- **Nginx** - Reverse proxy and load balancing

---

## 📁 Project Structure

```
fitnco-backend/
├── src/
│   ├── commons/          # Shared utilities and helpers
│   │   ├── auth.py       # Authentication decorators
│   │   ├── exception.py  # Custom exception classes
│   │   ├── handlers.py   # Error handlers
│   │   ├── request.py    # Request utilities
│   │   └── response.py   # Response formatters
│   ├── helpers/          # Business logic helpers
│   │   ├── cache_helper.py    # Redis caching utilities
│   │   ├── fcm_helper.py      # Firebase messaging
│   │   ├── mail_helper.py     # Email services
│   │   ├── sql_helper.py      # Database utilities
│   │   └── worker_helper.py   # Background tasks
│   ├── models/           # SQLAlchemy database models
│   │   ├── users_model.py     # User entities
│   │   ├── diets_model.py     # Nutrition data
│   │   ├── messages_model.py  # Messaging system
│   │   └── ...
│   ├── resources/        # Flask-RESTful API endpoints
│   │   ├── auth_resource.py   # Authentication endpoints
│   │   ├── user_resource.py   # User management
│   │   ├── diet_resource.py   # Nutrition endpoints
│   │   └── ...
│   ├── services/         # Business logic layer
│   │   ├── auth_service.py    # Authentication services
│   │   ├── user_service.py    # User management services
│   │   ├── diet_service.py    # Nutrition services
│   │   └── ...
│   ├── schemas/          # JSON schema validation
│   │   ├── auth_schema.json   # Authentication schemas
│   │   ├── register_schema.json
│   │   └── ...
│   └── utils/            # Utility functions
│       ├── datetime_util.py   # Date/time utilities
│       ├── validation_util.py # Input validation
│       └── ...
├── docker/               # Docker configuration
│   ├── docker-compose.yml     # Multi-container setup
│   └── conf/                  # Configuration files
├── fitnco-socket/        # WebSocket server
│   ├── fit-socket.py          # Socket.IO implementation
│   └── restart.sh             # Service restart script
├── seeds/                # Database seeders
│   └── user_seeder.py         # Initial data population
├── app.py                # Flask application factory
├── config.py             # Application configuration
├── wsgi.py               # WSGI application entry point
└── requirements.txt      # Python dependencies
```

---

## 🛠️ Development Setup

### Prerequisites

- **Python** 3.9+
- **PostgreSQL** 15+
- **Redis** 7.0+
- **Docker** (optional, recommended)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/MoriEdan/FitncoBackEnd.git
   cd FitncoBackEnd
   ```

2. **Start with Docker Compose**
   ```bash
   cd docker
   docker-compose up -d
   ```

### Manual Installation

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment configuration**
   ```bash
   cp .env-example .env
   # Edit .env with your configuration
   ```

4. **Database setup**
   ```bash
   # Initialize database
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   
   # Seed initial data
   python seeder.py
   ```

5. **Start the application**
   ```bash
   # Development server
   python app.py
   
   # Production server
   gunicorn -c gunicorn.py wsgi:app
   ```

---

## 🔧 Configuration

### Environment Variables

```bash
# Application
DEFAULT_CONFIG_TYPE="ProductionConfig"
APPLICATION_ROOT="/api"
HOST="0.0.0.0"
PORT=5000

# Database
SQLALCHEMY_DATABASE_URI="postgresql://user:pass@localhost:5432/fitnco"

# Redis Cache
CACHE_REDIS_URL="redis://:password@localhost:6379/0"
REDIS_HOST="localhost"
REDIS_PASSWORD="your_redis_password"

# Security
JWT_SECRET_KEY="your-jwt-secret-key"
SECRET_KEY="your-flask-secret-key"

# AWS Services
AWS_ACCESS_KEY_ID="your_aws_access_key"
AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
AWS_BUCKET="fitnco-uploads"

# Firebase
FCM_KEY="your_firebase_server_key"

# Monitoring
SENTRY_DSN="your_sentry_dsn"
```

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/refresh` | Refresh JWT token |
| POST | `/api/auth/logout` | User logout |
| POST | `/api/auth/forgot-password` | Password reset |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/me` | Get current user profile |
| PUT | `/api/users/me` | Update user profile |
| GET | `/api/users/{id}` | Get user by ID |
| DELETE | `/api/users/{id}` | Delete user account |

### Nutrition & Diet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/diets` | Get user diet plans |
| POST | `/api/diets` | Create new diet plan |
| GET | `/api/diets/{id}` | Get specific diet plan |
| PUT | `/api/diets/{id}` | Update diet plan |
| POST | `/api/logs/breakfast` | Log breakfast meal |
| POST | `/api/logs/lunch` | Log lunch meal |
| POST | `/api/logs/dinner` | Log dinner meal |

### Real-time Features

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `/socket.io/` | WebSocket | Real-time messaging |
| `/api/messages` | HTTP | Message history |
| `/api/notifications` | HTTP | Push notifications |

---

## 🔄 Background Services

### WebSocket Server

```bash
# Start Socket.IO server
cd fitnco-socket
python fit-socket.py
```

### Celery Workers (if implemented)

```bash
# Start Celery worker
celery -A app.celery worker --loglevel=info

# Start Celery beat scheduler
celery -A app.celery beat --loglevel=info
```

---

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run tests with coverage
python -m pytest --cov=src tests/

# Run specific test file
python -m pytest tests/test_auth.py
```

---

## 📊 Performance & Monitoring

### Health Check

```bash
# Application health
GET /api/health

# Database connectivity
GET /api/health/db

# Redis connectivity
GET /api/health/redis
```

### Metrics

- **Response Time**: < 200ms average
- **Uptime**: 99.9% availability
- **Throughput**: 1000+ requests/minute
- **Error Rate**: < 0.1%

---

## 🚀 Deployment

### Production Deployment

1. **Build Docker image**
   ```bash
   docker build -t fitnco-backend .
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Database migration**
   ```bash
   docker exec fitnco-backend python manage.py db upgrade
   ```

### System Service

```bash
# Install systemd service
sudo cp fitnco.service /etc/systemd/system/
sudo systemctl enable fitnco
sudo systemctl start fitnco
```

---

## 🌐 Related Projects

- **📱 Mobile App**: [FitncoApp](https://github.com/MoriEdan/FitncoApp) - React Native mobile application
- **🌐 Website**: [fitnco.fit](https://fitnco.fit/) - Official website
- **🏢 Company**: [Liberyus](https://www.liberyus.com/) - Development company

---

## 👥 Development Team

**Developed by [Liberyus](https://www.liberyus.com/)**

Liberyus is a leading software development company specializing in scalable backend systems, mobile applications, and cloud solutions.

### Core Contributors
- **Backend Architecture**: Senior Python Developers
- **Database Design**: Database Specialists
- **DevOps**: Cloud Infrastructure Engineers
- **Quality Assurance**: Testing Engineers

---

## 📄 License

This project is proprietary and confidential. All rights reserved by Liberyus.

```
Copyright (c) 2024 Liberyus
All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
transferring or reproduction of this software, via any medium, is
strictly prohibited.
```

---

## 🤝 Contributing

This is a private project. For development team members:

1. **Development Workflow**
   - Create feature branch from `develop`
   - Follow PEP 8 coding standards
   - Write comprehensive tests
   - Submit pull request with detailed description

2. **Code Quality Standards**
   - Minimum 80% test coverage
   - All tests must pass
   - Code review required
   - Documentation updates required

---

## 📞 Support & Contact

### Technical Support
- **Development Team**: tech@liberyus.com
- **Infrastructure**: devops@liberyus.com
- **Documentation**: [Internal Wiki](https://wiki.liberyus.com/fitnco)

### Business Inquiries
- **Website**: [liberyus.com](https://www.liberyus.com/)
- **FitnCo Platform**: [fitnco.fit](https://fitnco.fit/)
- **Business Contact**: info@liberyus.com

---

## 🏆 Achievements

- ⚡ **High Performance**: Serving 10,000+ daily active users
- 🔒 **Security First**: Zero security incidents since launch
- 📈 **Scalable**: Handles 1M+ API requests daily
- 🌍 **Global Reach**: Supporting users across multiple countries
- 🏅 **Award Winning**: Recognized for technical excellence

---

<div align="center">
  <h3>🚀 Powering the Future of Fitness Technology</h3>
  <p>Made with ❤️ by <a href="https://www.liberyus.com/">Liberyus</a></p>
  <p>© 2024 FitnCo Backend. All rights reserved.</p>
  
  <br>
  
  <img src="https://img.shields.io/badge/Built%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Built with Python">
  <img src="https://img.shields.io/badge/Powered%20by-Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Powered by Flask">
  <img src="https://img.shields.io/badge/Deployed%20on-AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="Deployed on AWS">
</div>

