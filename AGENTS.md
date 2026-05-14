AGENTS.md - Essential Instructions for OpenCode Sessions
Development Setup
- Start all services: docker-compose up -d
- Backend only: docker-compose up -d backend database
- Frontend only: docker-compose up -d frontend
- Stop services: docker-compose down
- View logs: docker-compose logs -f [service]
Backend Commands
- Run server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
- Run tests: pytest (run from backend directory)
- Create migration: alembic revision --autogenerate -m "message"
- Apply migrations: alembic upgrade head
- Install deps: pip install -r requirements.txt
Frontend Commands
- Dev server: npm run dev (runs on http://localhost:5173)
- Build: npm run build
- Preview: npm run preview
- Install deps: npm install
Architecture Notes
- Backend structure: Modular monolith with domain modules in app/modules/
- Each module has: router.py, service.py, repository.py, models.py, schemas.py
- Cross-cutting concerns: app/core/ (config, security, events_bus, etc.)
- Async workers: app/workers/ (image processing, webhooks, feeds)
- Shared code: app/shared/ (enums, utils, constants, mixins)
Testing
- Unit tests: backend/tests/unit/
- Integration tests: backend/tests/integration/
- E2E tests: backend/tests/e2e/
- Test command: pytest (from backend root)
Environment
- Env file: .env in backend root
- DB credentials: In docker-compose.yml (postgres/postgres/realestate)
- Frontend proxy: Configured to call backend at http://localhost:8000
Code Style
- Python: Follow PEP 8, use type hints
- JS/ESLint: Configured in frontend (React + Vite template)
- Commits: Conventional commits preferred (feat:, fix:, etc.)
Important Constraints
- Database: PostgreSQL 16 (defined in docker-compose)
- API Docs: Available at http://localhost:8000/docs when backend runs
- CORS: Configured for http://localhost:5173 (frontend dev URL)
- Auth: JWT-based (see app/core/security.py)