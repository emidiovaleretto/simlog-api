# flightsim-app

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

A Django-based web application designed for flight simulation enthusiasts.

The project aims to bring together tools and workflows commonly used in virtual aviation, including flight logging, operational checklists, user accounts, and integration with SimBrief flight planning data.

## Overview

`flightsim-app` is currently in the early stages of development. The project has been structured into focused Django apps to keep responsibilities separated and to support future growth in a clean and maintainable way.

### Current modules

- `accounts` — user-related features.
- `logbook` — flight logging and tracking.
- `checklist` — operational checklists.
- `services.py` — SimBrief API integration layer.

## Features so far

- Django project scaffold created.
- Environment variables managed through `.env`.
- SimBrief service layer prepared for fetching flight plan data.
- Project separated into modular apps for easier future expansion.

## Tech Stack

- Python
- Django
- Requests
- python-dotenv or environment-based configuration

## Project Structure

```bash
flightsim-app/
├── accounts/
├── checklist/
├── logbook/
├── core/
├── services.py
├── .env
├── requirements.txt
└── manage.py
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.10+.
- pip.
- Git.

### Clone the repository

```bash
git clone https://github.com/emidiovaleretto/flightsim-app.git
cd flightsim-app
```

### Create a virtual environment

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

If you later add more settings, such as API keys or database credentials, keep them in this file as well.

### Apply migrations

```bash
python manage.py migrate
```

### Run the development server

```bash
python manage.py runserver
```

Then open:

```bash
http://127.0.0.1:8000/
```

## SimBrief Integration

This project includes a service layer intended to consume SimBrief API data and extract flight information such as:

- origin.
- destination.
- aircraft.
- fuel planning.
- route.
- passenger count.

SimBrief is a flight planning platform widely used in virtual aviation, and its API is designed for developers who want to integrate dispatch and flight-planning data into their own tools [web:72][web:77].

## Roadmap

- Expand the accounts module.
- Build logbook and checklist workflows.
- Improve SimBrief data handling and error management.
- Add templates or API endpoints for displaying flight data.
- Add automated tests.
- Prepare the project for deployment.

## Contributing

This project is under active development. Contributions, suggestions, and issue reports are welcome.

## License

MIT
