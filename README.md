# 🎵 Video to MP3 Converter

A modern, scalable microservices-based video to MP3 conversion platform built with FastAPI, featuring user authentication, file processing, and email notifications.

## 🏗️ Architecture

This project follows a microservices architecture pattern with the following services:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gateway       │    │   Auth Service  │    │  Media Service  │
│   (Port 8000)   │◄──►│   (Port 5000)   │    │   (Port 7000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Convertor       │    │ Notification    │    │   RabbitMQ      │
│ Service         │    │ Service         │    │   Message       │
│ (Port 4000)     │    │ (Port 6000)     │    │   Broker        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MongoDB       │    │   PostgreSQL    │    │   Mongo Express │
│   (Port 27017)  │    │   (Port 5433)   │    │   (Port 8081)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Features

- **User Authentication**: JWT-based authentication with registration and login
- **Video Upload**: Secure file upload with GridFS storage
- **Video Processing**: Asynchronous video to MP3 conversion using FFmpeg
- **Email Notifications**: Automated welcome and conversion completion emails
- **API Gateway**: Centralized routing and request handling
- **Microservices**: Scalable, independent service architecture
- **Message Queuing**: RabbitMQ for asynchronous communication
- **Database Support**: PostgreSQL for user data, MongoDB for file storage

## 🛠️ Tech Stack

### Backend Services
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.13** - Programming language
- **SQLModel** - Database ORM with type safety
- **Pydantic** - Data validation and settings management

### Databases
- **PostgreSQL 17** - Relational database for user management
- **MongoDB 6.0** - Document database with GridFS for file storage

### Message Queue
- **RabbitMQ 3.12** - Message broker for asynchronous communication

### Media Processing
- **FFmpeg** - Video/audio processing and conversion

### Email Service
- **FastAPI-Mail** - Email sending capabilities

### Infrastructure
- **Docker & Docker Compose** - Containerization and orchestration
- **Uvicorn** - ASGI server for FastAPI applications

## 📁 Project Structure

```
video-mp3-convertor/
├── docker-compose.dev.yml          # Development environment setup
└── services/
    ├── auth/                       # Authentication service
    │   ├── src/
    │   │   ├── auth/              # Auth module
    │   │   │   ├── routes.py      # API endpoints
    │   │   │   ├── service.py     # Business logic
    │   │   │   ├── schema.py      # Data models
    │   │   │   └── utils.py       # Utilities (JWT, hashing)
    │   │   └── db/                # Database configuration
    │   └── requirements.txt
    ├── convertor/                  # Video conversion service
    │   ├── main.py                # Service entry point
    │   ├── mp3_consumer.py        # RabbitMQ consumer
    │   └── requirements.txt
    ├── gateway/                    # API Gateway
    │   ├── main.py                # Proxy service
    │   └── requirements.txt
    ├── media/                      # Media handling service
    │   ├── src/
    │   │   ├── media/             # Media module
    │   │   │   ├── routes.py      # Upload/download endpoints
    │   │   │   └── service.py     # File operations
    │   │   └── auth.py            # Authentication middleware
    │   └── requirements.txt
    └── notification/               # Email notification service
        ├── src/
        │   ├── consumer/          # Message consumers
        │   │   ├── mp3_consumer.py    # Conversion notifications
        │   │   └── user_consumer.py   # Welcome emails
        │   └── mail.py            # Email configuration
        └── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd video-mp3-convertor
   ```

2. **Start the services**
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```

3. **Access the services**
   - **API Gateway**: http://localhost:8000
   - **Auth Service**: http://localhost:5000
   - **Media Service**: http://localhost:7000
   - **RabbitMQ Management**: http://localhost:15672 (admin/pass)
   - **Mongo Express**: http://localhost:8081 (admin/pass)

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/sign-up
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Login User
```http
POST /auth/sign-in
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Verify Token
```http
GET /auth/verify
Authorization: Bearer <access_token>
```

### Media Endpoints

#### Upload Video
```http
POST /media/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

file: <video_file>
```

#### Download MP3
```http
GET /media/download/{file_id}
Authorization: Bearer <access_token>
```

## 🔄 Workflow

1. **User Registration/Login**: Users authenticate through the auth service
2. **Video Upload**: Users upload videos through the media service
3. **File Storage**: Videos are stored in MongoDB using GridFS
4. **Message Queue**: Upload event triggers RabbitMQ message
5. **Video Processing**: Convertor service processes videos to MP3 using FFmpeg
6. **Notification**: Email notification sent when conversion is complete
7. **Download**: Users can download converted MP3 files

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| Gateway | 8000 | API Gateway and routing |
| Auth | 5000 | User authentication |
| Media | 7000 | File upload/download |
| Convertor | 4000 | Video processing |
| Notification | 6000 | Email notifications |
| PostgreSQL | 5433 | User database |
| MongoDB | 27017 | File storage |
| RabbitMQ | 5672 | Message broker |
| RabbitMQ Management | 15672 | Message queue UI |
| Mongo Express | 8081 | MongoDB UI |

## 🔧 Environment Variables

### Auth Service
- `JWT_SECRET`: Secret key for JWT token generation
- `DATABASE_URL`: PostgreSQL connection string
- `RABBITMQ_URL`: RabbitMQ connection string

### Media Service
- `RABBITMQ_URL`: RabbitMQ connection string
- `MONGODB_URL`: MongoDB connection string
- `AUTH_URL`: Auth service URL for token validation

### Convertor Service
- `RABBITMQ_URL`: RabbitMQ connection string
- `MONGODB_URL`: MongoDB connection string

### Gateway Service
- `AUTH_URL`: Auth service URL
- `MEDIA_URL`: Media service URL

## 🧪 Development

### Running Individual Services

Each service can be run independently:

```bash
# Auth Service
cd services/auth
python -m uvicorn src.main:app --host 0.0.0.0 --port 5000

# Media Service
cd services/media
python -m uvicorn src.main:app --host 0.0.0.0 --port 7000

# Gateway Service
cd services/gateway
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Database Migrations

The auth service uses SQLModel with automatic table creation. For production, consider using Alembic for migrations.

## 🔒 Security Features

- JWT-based authentication with access and refresh tokens
- Password hashing using bcrypt
- Token-based authorization for protected endpoints
- Secure file upload with validation
- Environment-based configuration

## 📈 Scalability

- Microservices architecture allows independent scaling
- Message queue enables asynchronous processing
- Stateless services for horizontal scaling
- Database separation for different data types

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Future Enhancements

- [ ] WebSocket support for real-time conversion progress
- [ ] Multiple output formats (WAV, AAC, etc.)
- [ ] Batch processing capabilities
- [ ] User dashboard with conversion history
- [ ] File size and format validation
- [ ] Rate limiting and usage quotas
- [ ] Cloud storage integration (AWS S3, Google Cloud)
- [ ] Kubernetes deployment configuration
- [ ] Monitoring and logging with Prometheus/Grafana
- [ ] CI/CD pipeline setup

---

**Built with ❤️ using FastAPI and modern Python practices**
