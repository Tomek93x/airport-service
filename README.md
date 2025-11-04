# Airport Service API

A Django REST API for tracking flights and managing airport operations.  
This project is built as a portfolio-ready, Dockerized backend for booking and administration of airports, flights, crews, and ticket orders.

## Features

- JWT Authentication for secure access
- Full CRUD for Airports, Routes, Airplanes, Crews, and Orders
- Flight management and seat booking system
- Image upload support for airplanes
- Filtering and search for flights (by route, date)
- Automatic pagination and rate limiting
- Cross-Origin Resource Sharing (CORS) support for frontend integration
- Admin panel for easy data management
- API documentation with Swagger and ReDoc
- CI-ready and PEP8-compliant codebase
- Docker and docker-compose support

## Technology Stack

- Python 3.11+
- Django 4.2+
- Django REST Framework
- PostgreSQL (Docker) or SQLite
- JWT authentication
- drf-spectacular (OpenAPI docs)
- Docker, Docker Compose

## Installation

### Local Development

1. **Clone the repository**
    ```
    git clone https://github.com/yourusername/airport-service.git
    cd airport-service
    ```

2. **Create a virtual environment**
    ```
    python -m venv venv
    source venv/bin/activate        # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**
    ```
    pip install -r requirements.txt
    ```

4. **Run migrations**
    ```
    python manage.py migrate
    ```

5. **Create superuser**
    ```
    python manage.py createsuperuser
    ```

6. **Run development server**
    ```
    python manage.py runserver
    ```
    The API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Docker Development

1. **Build and run containers**
    ```
    docker-compose up --build
    ```
2. **Create superuser in running container**
    ```
    docker-compose exec app python manage.py createsuperuser
    ```
3. The API and docs will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## API Endpoints

### Authentication
- `POST /api/token/` – Obtain JWT token
- `POST /api/token/refresh/` – Refresh JWT token

### Airports
- `GET /api/airport/airports/` – List all airports
- `POST /api/airport/airports/` – Create airport

### Routes
- `GET /api/airport/routes/` – List all routes
- `POST /api/airport/routes/` – Create route *(admin only)*
- `GET /api/airport/routes/{id}/` – Route details

### Airplanes
- `GET /api/airport/airplanes/` – List all airplanes
- `POST /api/airport/airplanes/` – Create airplane *(admin only)*
- `POST /api/airport/airplanes/{id}/upload-image/` – Upload airplane image *(admin only)*

### Flights
- `GET /api/airport/flights/` – List all flights  
  Supports filtering: `?source=Warsaw&destination=NewYork&date=2025-12-01`
- `POST /api/airport/flights/` – Create flight *(admin only)*
- `GET /api/airport/flights/{id}/` – Flight details

### Orders
- `GET /api/airport/orders/` – List user's orders
- `POST /api/airport/orders/` – Book tickets
- `GET /api/airport/orders/{id}/` – Order details

### Crews & Airplane Types
- `GET /api/airport/crews/` – List crews
- `POST /api/airport/crews/` – Add crew
- `GET /api/airport/airplane-types/` – List types
- `POST /api/airport/airplane-types/` – Add type

## API Documentation

- **Swagger UI:** [http://127.0.0.1:8000/api/doc/swagger/](http://127.0.0.1:8000/api/doc/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/api/doc/redoc/](http://127.0.0.1:8000/api/doc/redoc/)
- **Admin panel:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Examples

### 1. Obtain JWT token
