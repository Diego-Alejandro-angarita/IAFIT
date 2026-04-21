# IAFIT Agent Instructions

This repository is a full-stack application with an Angular frontend and a Django backend that integrates RAG via `llama-index`.

## Architecture & Boundaries

- **Frontend (`Frontend/frontend-rag/`):** Angular 21 with SSR (`@angular/ssr`). Uses Bootstrap and Leaflet.
- **Backend (`Backend/`):** Django application using Django REST Framework. The main application logic resides in the `LlamaIndex` app.
- **Database:** Supabase PostgreSQL. While a `db.sqlite3` may exist locally, the production/default database in `settings.py` depends on the `SUPABASE_DB_URL` environment variable.

## Setup & Environment Quirks

- The Python virtual environment is located at the repository root (`.venv` or `venv`), but all backend commands must be run from the `Backend/` directory.
- **Backend Environment Variables:** You must have a `.env` file inside the `Backend/` directory. Required keys include `SUPABASE_DB_URL`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `GEMINI_API_KEY`, and `LLAMAINDEX_API_KEY`.
- **CORS:** The Django backend is configured to accept requests from the Angular dev server at `http://localhost:4200` and `http://127.0.0.1:4200`.

## Developer Commands

- **Backend:** Run `python manage.py runserver` from within the `Backend/` directory.
- **Frontend:** Run `npm start` from within the `Frontend/frontend-rag/` directory.
- **VS Code Tasks:** There are pre-configured VS Code tasks (`Start Full Stack`) to start both the frontend and backend in parallel.
- **Scripts:** Custom Django seeding and migration scripts exist in `Backend/scripts/` (e.g., `seed_establishments.py`). Run these from the `Backend/` directory like so: `python scripts/seed_establishments.py`.

## Testing

- Frontend unit tests use Vitest: `npm run test` (from `Frontend/frontend-rag/`).
- Backend tests should follow standard Django conventions (`python manage.py test LlamaIndex`).
