# Expo + Python FastAPI Template

A full-stack mobile application template combining Expo (React Native) frontend with Python FastAPI backend API.

## Project Structure

```
.
├── api/                  # Python FastAPI backend
│   ├── main.py          # FastAPI app entry point
│   ├── requirements.txt # Python dependencies
│   ├── seed_data.py     # Database seeding
│   └── app/
│       ├── core/        # Core configuration
│       ├── models/      # SQLAlchemy models
│       ├── schemas.py   # Pydantic schemas
│       └── api/v1/      # API endpoints
├── config/              # Frontend configuration
│   └── api.ts          # API endpoint configuration
├── app/                # Expo Router pages
├── components/         # React components
├── services/           # API services
├── stores/            # Zustand state stores
└── .env               # Environment variables
```

## Installation

### Prerequisites

* Node.js and npm

    ```bash
    $ node --version  # output should be 18.x or higher
    $ npm --version   # output should be 8.x or higher
    ```

* Python 3.x

    ```bash
    $ python3 --version  # output should be 3.9 or higher
    ```

* PostgreSQL

    ```bash
    $ brew install postgresql
    ```

### Setup

1. Install frontend dependencies:

    ```bash
    $ npm install
    ```

2. Setup backend (Python FastAPI):

    ```bash
    $ cd api
    $ python3 -m pip install -r requirements.txt
    ```

3. Configure environment variables:

    Copy `.env.example` to `.env` and adjust settings:

    ```bash
    $ cp .env.example .env
    ```

4. Seed database (optional):

    ```bash
    $ cd api
    $ python3 seed_data.py
    ```

## Configuration

Environment variables in `.env`:

```bash
# FastAPI backend port
APP_PORT=3001

# Expo web server port (frontend runs on 3000)
EXPO_WEB_PORT=3000
```

Backend configuration in `api/app/core/config.py`:

```python
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/dbname"
SECRET_KEY = "your-secret-key"
```

## Development

Start backend and frontend:

**Option 1 - Using npm scripts:**
```bash
$ npm run start-backend  # Start FastAPI backend (port 3001)
$ npm run start         # Start Expo frontend
```

**Option 2 - Manual start:**

**Terminal 1 - Backend API:**
```bash
$ cd api
$ python3 -m uvicorn main:app --host 0.0.0.0 --port 3001 --reload
```
Backend will start on port **3001**: http://localhost:3001

**Terminal 2 - Frontend:**
```bash
$ npm run start   # Start Metro bundler
$ npm run web     # Start web development (port 3000)
$ npm run ios     # Start iOS simulator
$ npm run android # Start Android emulator
```

Frontend web will start on port **3000**: http://localhost:3000

## API Endpoints

The backend provides RESTful API endpoints:

### Health Check
* `GET /api/v1/health` - Health check endpoint

### Authentication
* `POST /api/v1/registrations` - User registration
* `POST /api/v1/sessions` - User login
* `DELETE /api/v1/sessions` - User logout

### Calculators
* `GET /api/v1/calculators` - List all calculators
* `GET /api/v1/calculators/{id}` - Get calculator by ID

### Calculation Results
* `GET /api/v1/calculation_results` - List user's calculation history
* `POST /api/v1/calculation_results` - Create new calculation
* `GET /api/v1/calculation_results/{id}` - Get calculation result by ID
* `DELETE /api/v1/calculation_results/{id}` - Delete calculation result

### User Profile
* `GET /api/v1/profile` - Get current user profile
* `PATCH /api/v1/profile` - Update user profile

Example requests:
```bash
$ curl http://localhost:3001/api/v1/health
# {"status":"healthy"}

$ curl http://localhost:3001/api/v1/calculators
# [{"id":1,"name":"Body Mass Index (BMI)","description":"...","formula":"..."}]
```

## Authentication

The app includes JWT-based authentication system with:
* User registration with email/password
* Secure password hashing (bcrypt)
* JWT token generation and validation
* Protected API endpoints
* Session management with SecureStore

Frontend usage:
```typescript
import { useAuth } from '@/hooks/useAuth';

const { user, login, logout } = useAuth();

// Login
await login(email, password);

// Logout
await logout();
```

## Tech Stack

### Frontend (Expo)
* React Native 0.74.5
* Expo SDK ~51.0
* Expo Router ~3.5 (file-based routing)
* NativeWind v4 (Tailwind CSS for React Native)
* TypeScript ~5.3
* React 18.2
* Zustand (state management)

### Backend (Python FastAPI)
* Python 3.x
* FastAPI 0.115.5 (async web framework)
* SQLAlchemy 2.0.36 (async ORM)
* PostgreSQL (via asyncpg)
* Pydantic 2.10.3 (data validation)
* JWT authentication (python-jose)
* Uvicorn (ASGI server)
* Bcrypt (password hashing)

## Testing

### Frontend Tests
```bash
$ npm test        # Run all tests (Jest + ESLint + TypeScript)
$ npm run lint    # Run linting only
```

### Backend Tests
```bash
$ cd api
$ python -m pytest
```

## Generators

### API Client Generator

Generate types, services, and stores for a new resource:

```bash
$ npm run gen api RESOURCE [actions...]
```

Example:
```bash
$ npm run gen api posts index show create update
```

This generates:
* `types/posts.ts` - TypeScript types
* `services/posts.ts` - API service functions
* `stores/postsStore.ts` - Zustand store

### Authentication Generator

Generate complete authentication system:

```bash
$ npm run gen authentication
```

This generates:
* Authentication types (`types/auth.ts`)
* Auth service (`services/auth.ts`)
* Auth context (`contexts/AuthContext.tsx`)
* Auth hook (`hooks/useAuth.ts`)
* Auth screens (`app/(auth)/sign-in.tsx`, `sign-up.tsx`, `forgot-password.tsx`)

## Deployment

### Environment Configuration

The app uses the same environment variables for both frontend and backend:

* **Local dev**: Uses `APP_PORT` from `.env`
* **Cloud dev**: Reads system-injected `APP_PORT` + `CLACKY_PREVIEW_DOMAIN_BASE`
* **Production**: Uses `PUBLIC_HOST` for the API domain

All configuration is managed through `app.config.js` and automatically maps to the appropriate format.

## License

MIT
