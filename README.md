# simlog-api

![CI](https://github.com/emidiovaleretto/simlog-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.15-092E20?style=flat&logo=django&logoColor=ff1709)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

Backend REST API for **simlog** — a SaaS companion app for Microsoft Flight Simulator 2024 pilots. Manage your flight logbook, aircraft checklists and import flight plans directly from SimBrief.

**Live API:** https://api.simlog.app.br/api/flights/

> **simlog-app** (React frontend) → coming soon

---

## Features

- **Flight Logbook** — log flights with origin, destination, aircraft, duration, score and notes. Filter by origin, destination or aircraft. Search in notes. Paginated responses.
- **Checklist Manager** — create aircraft profiles with custom checklists and items per flight phase. Track active sessions with completed items.
- **SimBrief Integration** — fetch your latest flight plan and import it directly into the logbook with one request.
- **JWT Authentication** — secure endpoints with access and refresh tokens. User profiles with SimBrief pilot ID.
- **Stats Dashboard** — total flights, hours, airports visited, average score, most flown aircraft and most visited airports.
- **Picture Profile** — upload with automatic resizing (400px) and JPEG conversion.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | Django 5.x + Django REST Framework |
| Auth | JWT (djangorestframework-simplejwt) |
| Database | PostgreSQL 15 (production) / SQLite (development) |
| Config | python-decouple |
| Testing | pytest + pytest-django + factory-boy |
| Linting | flake8 |
| Security | bandit |
| CI/CD | GitHub Actions |
| Containers | Docker + docker-compose |
| Deploy/Hosting | Railway |
---

## API Endpoints

### Authentication
```
POST   /api/auth/register/        Register a new user
POST   /api/auth/login/           Login and get JWT tokens
POST   /api/auth/token/refresh/   Refresh access token
GET    /api/auth/me/              Get current user profile
PUT    /api/auth/me/              Update profile (simbrief_pilot_id)
```

### Flight Logbook
```
GET    /api/flights/              List flights (paginated, filterable)
POST   /api/flights/              Create a flight
GET    /api/flights/{id}/         Get flight detail
PUT    /api/flights/{id}/         Update a flight
DELETE /api/flights/{id}/         Delete a flight
GET    /api/flights/stats/        Get logbook stats
```

**Query parameters:**
```
?origin=EIDW          Filter by origin ICAO
?destination=KJFK     Filter by destination ICAO
?aircraft=A320        Filter by aircraft name
?search=Atlantic      Search in notes
```

### Checklist Manager
```
GET    /api/aircraft/                         List aircraft
POST   /api/aircraft/                         Create aircraft
GET    /api/aircraft/{id}/                    Aircraft detail (with checklists)
PUT    /api/aircraft/{id}/                    Update aircraft
DELETE /api/aircraft/{id}/                    Delete aircraft
GET    /api/aircraft/{id}/checklists/         List checklists
POST   /api/aircraft/{id}/checklists/         Create checklist
GET    /api/checklists/{id}/                  Checklist detail (with items)
PUT    /api/checklists/{id}/                  Update checklist
DELETE /api/checklists/{id}/                  Delete checklist
GET    /api/checklists/{id}/items/            List items
POST   /api/checklists/{id}/items/            Create item
GET    /api/items/{id}/                       Item detail
PUT    /api/items/{id}/                       Update item
DELETE /api/items/{id}/                       Delete item
POST   /api/sessions/                         Start a flight session
PATCH  /api/sessions/{id}/                    Update completed items
GET    /api/sessions/{id}/                    Get session
```

### SimBrief
```
GET    /api/simbrief/latest/      Fetch latest flight plan
POST   /api/simbrief/import/      Import plan into logbook
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker Desktop
- Git

### Clone the repository

```bash
git clone https://github.com/emidiovaleretto/simlog-api.git
cd simlog-api
```

### Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values:

```env
SECRET_KEY=your-secret-key-here-must-be-at-least-32-chars
DEBUG=True
DB_NAME=simlog
DB_USER=simlog_user
DB_PASSWORD=simlog_password
DB_HOST=db  # use 'localhost' if running without Docker
DB_PORT=5432
```

### Start with Docker

```bash
docker compose up --build
```

### Run migrations

```bash
docker compose run --rm -it api python3 manage.py migrate
```

The API will be available at `http://localhost:8000`.

---

## Running Tests

```bash
# All tests
docker compose run --rm -it api python3 -m pytest tests/ -v

# Specific file
docker compose run --rm -it api python3 -m pytest tests/test_accounts.py -v

# Code style
docker compose run --rm -it api python3 -m flake8 . --max-line-length=120

# Security
docker compose run --rm -it api python3 -m bandit -r . --exclude .venv,migrations -ll
```

**Current test coverage: 69 tests across 5 test files.**

| File | Tests |
|---|---|
| test_accounts.py | 15 |
| test_logbook.py | 17 |
| test_checklist.py | 20 |
| test_simbrief.py | 10 |
| test_logbook_enhancements.py | 7 |

---

## Project Structure

```
simlog-api/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI
├── accounts/                   # Auth and user profiles
│   ├── models.py               # UserProfile
│   ├── serializers.py
│   ├── views.py                # RegisterView, MeView
│   └── urls.py
├── checklist/                  # Checklist manager
│   ├── models.py               # Aircraft, Checklist, ChecklistItem, FlightSession
│   ├── serializers.py
│   ├── signals.py              # Auto-create User Profile
│   ├── views.py
│   ├── urls.py
│   └── utils.py                # Image processing
├── logbook/                    # Flight logbook
│   ├── models.py               # Flight
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── simbrief/                   # SimBrief integration
│   ├── services.py             # SimBriefService
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── core/                       # Project config
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── docker.py
│   │   └── production.py
│   │   └── testing.py
│   └── urls.py
├── tests/                      # Test suite
│   ├── factories.py
│   ├── test_accounts.py
│   ├── test_logbook.py
│   ├── test_checklist.py
│   ├── test_simbrief.py
│   └── test_logbook_enhancements.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .flake8
└── manage.py
```

---

## Development Notes

**Settings are split into four files:**
- `base.py` — shared across all environments
- `development.py` — SQLite, DEBUG=True
- `docker.py` — PostgreSQL, used by Docker and CI
- `production.py` — PostgreSQL, DEBUG=False
- `testing.py` — SQLite, DEBUG=True

**ICAO codes are always validated and uppercased** on origin and destination fields.

**Duration is auto-calculated** from departure and arrival times on the Flight model.

**SimBrief requests use a 10-second timeout** to prevent hanging connections.

---

## Roadmap

- Social login (Google & GitHub)
- Profile picture placeholder
- Cloud storage for media (Cloudinary)
- Health check endpoint + API status page
- React frontend (simlog-app)

See the [open issues](https://github.com/emidiovaleretto/simlog-api/issues) for a full list of proposed features.

---

## License

MIT
