# SolisoAPS 🚀

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=flat&logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-16+-339933?style=flat&logo=node.js)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A modern, full-stack web application featuring two Vue.js frontends (admin and user interface) and a FastAPI backend, designed for efficient administration and user interaction.

## ✨ Features

- **Frontend (Admin)**
  - Vue.js 3 with Composition API
  - Vite for lightning-fast development
  - TailwindCSS for responsive design
  - Vue Router for seamless navigation
  - Axios for HTTP requests
  - ESLint & Prettier for code quality
  - Comprehensive admin dashboard
  - User management system
  - Analytics and reporting

- **Frontend (User)**
  - Vue.js 3 with Composition API
  - Vite for optimal performance
  - TailwindCSS for responsive design
  - Vue Router for smooth navigation
  - Axios for API communication
  - User-friendly interface
  - Real-time updates
  - Mobile-first approach

- **Backend**
  - FastAPI for high-performance API
  - SQLAlchemy ORM for database operations
  - Automatic API documentation with Swagger UI
  - Async support for better performance
  - JWT authentication
  - CORS middleware
  - Role-based access control

## 📋 Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- npm or yarn
- pip

## 🚀 Getting Started

### Frontend Setup (Admin)

1. Navigate to the admin directory:
   ```bash
   cd admin
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Frontend Setup (User)

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
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

4. Start the backend server:
   ```bash
   python run.py
   ```

## 📁 Project Structure

```
SolisoAPS/
├── admin/                 # Admin Frontend Vue.js application
│   ├── src/              # Source files
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page components
│   │   ├── router/       # Vue Router configuration
│   │   ├── store/        # Vuex store
│   │   └── api/          # API service
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
├── frontend/             # User Frontend Vue.js application
│   ├── src/              # Source files
│   │   ├── components/   # Vue components
│   │   ├── views/        # Page components
│   │   ├── router/       # Vue Router configuration
│   │   ├── store/        # Vuex store
│   │   └── api/          # API service
│   ├── public/           # Static assets
│   └── package.json      # Frontend dependencies
└── backend/              # Backend FastAPI application
    ├── app/              # Backend source code
    │   ├── api/          # API endpoints
    │   ├── core/         # Core functionality
    │   ├── models/       # Database models
    │   └── schemas/      # Pydantic schemas
    ├── requirements.txt  # Python dependencies
    └── run.py           # Application entry point
```

## 🛠 Development

### Frontend Development

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

### Backend Development

- The backend server runs on `http://localhost:8000`
- API documentation is available at `http://localhost:8000/docs`
- Swagger UI for interactive API testing at `http://localhost:8000/docs`

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and follow our code style guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by the SolisoAPS Team
