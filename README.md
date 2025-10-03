# pythonBeer

A full-stack application for managing beer events, ratings, and user participation. The project consists of a Python-based API backend and a Nuxt.js client frontend.

## Features

- User authentication and registration
- Beer catalog management
- Event creation and participant management
- Beer ratings and toplists
- Real-time beer rating with Socket.IO
- RESTful API with database migrations and seed scripts
- Modern frontend with event and beer views

## Real-Time Features

This project uses Socket.IO to enable real-time interactions:
- Multiple users can rate beers simultaneously, with updates instantly reflected across all connected clients.
- Event participants see live updates to ratings and toplists without needing to refresh.
- Socket.IO integration ensures a dynamic and interactive experience during beer events.

## Project Structure

- `api/` — Python backend (FastAPI/Flask style)
  - Models, routes, schemas, services, and database setup
  - Alembic migrations for schema changes
  - Seed scripts for test data
  - Docker support for easy deployment
- `client/` — Nuxt.js frontend
  - Vue components for beers, events, ratings, and modals
  - TypeScript services and composables
  - Authentication middleware
  - Unit tests for components and services

## Getting Started

### Backend

1. Install dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   alembic upgrade head
   ```
3. Seed the database (optional):
   ```bash
   python seeds/populate-test-data.py
   ```
4. Start the API server:
   ```bash
   uvicorn app:app --reload
   ```
5. Run tests:
   ```bash
   pytest
   ```

### Frontend

1. Install dependencies:
   ```bash
   cd client
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev | npm run dev -- -o
   ```
3. Run frontend tests:
   ```bash
   npm run test
   ```

## Docker

To run the backend with Docker:
```bash
cd api
docker-compose up --build
docker compose exec web python -m seeds.populate-test-data
```

## Testing

- Backend: Uses `pytest` for unit and integration tests. Test coverage includes models, routes, services, and real-time event handling.
- Frontend: Uses `vitest` for Vue component and service testing. Simulates user interactions and real-time updates.
- To run all tests:
  - Backend: `pytest`
  - Frontend: `npm run test`

## Dependencies
- Node < 22
- Python < 3.8
- Docker

## Contributing

- Fork the repo and create a feature branch
- Submit pull requests with clear descriptions
- Run tests before submitting changes

## License

MIT
