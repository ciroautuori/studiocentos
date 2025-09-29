# SolisoAPS - Event and Project Management API

A FastAPI-based REST API for managing events and projects with image upload capabilities.

## Features

- **Event Management**
  - Create, read, update, and delete events
  - Filter events by featured status and upcoming dates
  - Image upload support for event media
  - Pagination support

- **Project Management**
  - Create, read, update, and delete projects
  - Filter active/inactive projects
  - Thumbnail upload support
  - Pagination support

## Technology Stack

- **Backend Framework:** FastAPI
- **Database:** SQLite with SQLAlchemy ORM
- **File Storage:** Local file system
- **Documentation:** OpenAPI (Swagger UI)

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SolisoAPS.git
cd SolisoAPS/backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
DATABASE_URL=sqlite:///./app.db
API_PREFIX=/api/v1
DEBUG=True
```

### Running the Application

1. Start the server:
```bash
python run.py
```

2. Access the API documentation:
- Swagger UI: http://localhost:8001/api/v1/docs
- ReDoc: http://localhost:8001/api/v1/redoc

## API Endpoints

### Events

- `GET /api/v1/events/` - List all events
- `GET /api/v1/events/{event_id}` - Get specific event
- `POST /api/v1/events/` - Create new event
- `PUT /api/v1/events/{event_id}` - Update event
- `DELETE /api/v1/events/{event_id}` - Delete event

### Projects

- `GET /api/v1/projects/` - List all projects
- `GET /api/v1/projects/{project_id}` - Get specific project
- `POST /api/v1/projects/` - Create new project
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Core configurations
│   ├── crud/          # Database operations
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   └── static/        # Static files storage
├── requirements.txt   # Python dependencies
├── run.py            # Application entry point
└── .env              # Environment variables
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.