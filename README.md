# Aktos.ai API

Aktos Engineering Take Home made by Ignacio Furey 
A RESTful API service built with Django and Django REST Framework.

## Whats missing before launching

### 1. Security
- **Authentication and Authorization**
- **Data Protection**
- **Attack Prevention**

### 2. Monitoring & Logging
- **System Monitoring**
- **Logging**
- **Alerting**

### 3. Data Integrity
- **Proper DB** not SQLlite

### 4. Pre-Post commits
- **Linter**
- **Migrations integrity check**

### 5. Versioning
- **Package manager**

### 6. Deployment
- **Brnaching strategy**
- **CI/CD**

## Setup

### Option 1: Local Development

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

### Option 2: Docker

1. Build the Docker image:
```bash
docker build -t aktos-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 aktos-api
```

The API will be available at:
- Main API: http://localhost:8000/api/
- Admin interface: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/swagger/

To see the logs:
```bash
docker logs -f <container_id>
```

To stop the container:
```bash
docker ps  # get the container ID
docker stop <container_id>
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
- Docker
