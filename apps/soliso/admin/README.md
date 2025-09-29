# SolisoAPS Admin Dashboard

A modern Vue.js admin dashboard for managing events and projects with a clean, responsive interface.

## Features

- **Project Management**
  - Create, read, update, and delete projects
  - Image upload support
  - Status tracking 
  - Active/Inactive filtering
  - Rich form validation

- **Event Management** 
  - Full event lifecycle management
  - Date range scheduling
  - Featured events support
  - Image upload capabilities
  - Location tracking

## Technology Stack

- **Frontend Framework:** Vue 3
- **Build Tool:** Vite
- **UI Framework:** Tailwind CSS
- **HTTP Client:** Axios
- **Router:** Vue Router
- **Code Quality:** ESLint + Prettier
- **Development Environment:** Node.js 16+

## Prerequisites

- Node.js 16.x or later
- npm 7.x or later
- A running instance of the SolisoAPS backend API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SolisoAPS.git
cd SolisoAPS/admin
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment (create `.env` file):
```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Development

Start the development server with hot-reload:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Code Quality

Run linting:
```bash
npm run lint
```

Format code:
```bash
npm run format
```

## Project Structure

```
admin/
├── src/
│   ├── assets/          # Static assets and global styles
│   ├── components/      # Reusable Vue components
│   ├── router/          # Vue Router configuration
│   ├── services/        # API services
│   ├── utils/           # Utility functions
│   ├── views/           # Page components
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── public/             # Public static assets
└── vite.config.js     # Vite configuration
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Vue.js team for the excellent framework
- Tailwind CSS for the utility-first CSS framework
- All contributors who participate in this project
