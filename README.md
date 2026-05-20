# simlog-api

![CI](https://github.com/emidiovaleretto/simlog-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

A Django REST API for flight simulation enthusiasts. The project brings together tools and workflows commonly used in virtual aviation, including flight logging, operational checklists, user accounts, and integration with SimBrief flight planning data.

## Overview

`simlog-api` is the backend service for the **simlog** app — a companion app for Microsoft Flight Simulator. It exposes a REST API consumed by the React Native mobile app.

### Current modules

- `accounts` — user authentication and profiles.
- `logbook` — flight logging and tracking.
- `checklist` — operational checklists per aircraft.
- `simbrief` — SimBrief API integration layer.

## Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt
- python-decouple
- PostgreSQL (production) / SQLite (development)
- pytest + flake8 + bandit (CI)

## Project Structure

```bash
simlog-api/
├── accounts/
├── checklist/
├── logbook/
├── simbrief/
│   └── services.py
├── core/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env.example
├── pytest.ini
├── .flake8
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3.12+
- pip
- Git

### Clone the repository

```bash
git clone https://github.com/emidiovaleretto/simlog-api.git
cd simlog-api
```

### Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements/development.txt
```

### Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in the required values.

### Apply migrations

```bash
python3 manage.py migrate
```

### Run the development server

```bash
python3 manage.py runserver
```

Then open: http://127.0.0.1:8000/

## Running Tests

```bash
python3 -m pytest
```

## SimBrief Integration

This project includes a service layer to consume SimBrief API data and extract flight information such as origin, destination, aircraft, fuel planning, route and passenger count.

## Roadmap

See the [open issues](https://github.com/emidiovaleretto/simlog-api/issues) for a full list of proposed features and known issues.

## License

MIT
