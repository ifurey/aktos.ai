# Aktos.ai API

Aktos Engineering Take Home made by Ignacio Furey 
A RESTful API service built with Django and Django REST Framework.

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aktos.ai.git
cd aktos.ai
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file (copy from .env.example):
```bash
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- JSON Schema: `http://localhost:8000/swagger.json`

## Project Structure

- `aktos_ai/` - Main package directory
  - `apps/` - Django applications
    - `api/` - API endpoints and services
  - `config/` - Project configuration

## Technology Stack

- Python 3.12.10
- Django 5.0.2
- Django REST Framework
- SQLite (Database)
- drf-yasg (API Documentation)
