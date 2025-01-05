# Stock Image Management Application

This is a Django-based application for managing stock images. It includes user authentication, image upload, and image management features.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Accessing the Deployed Version](#accessing-the-deployed-version)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- User registration and authentication
- Email verification
- Password reset
- Image upload and management
- Image reordering

## Technologies Used

- Django
- Django REST Framework
- Celery
- Redis
- PostgreSQL
- Docker
- Gunicorn

## Setup Instructions

### Prerequisites

- Python 3.11
- Docker
- Docker Compose

### Clone the Repository

```sh
git clone https://github.com/Aditya-Naresh/ImageStock-backend.git
cd ImageStock-backend
```

### Environment Variables

Create a `.env` file in the `mysite` directory and add the following environment variables:

```env
SECRET_KEY=<your-secret-key>
DB_URL=<your-database-url>
EMAIL_BACKEND=<your-email-backend>
EMAIL_HOST=<your-email-host>
EMAIL_USE_TLS=<your-email-use-tls>
EMAIL_PORT=<your-email-port>
EMAIL_HOST_USER=<your-email-host-user>
EMAIL_HOST_PASSWORD=<your-email-host-password>
FRONTEND=<your-frontend-url>
```

### Build and Run Docker Containers

```sh
docker-compose up --build
```

This will build and start the Docker containers for the web application, Redis, and PostgreSQL.

### Apply Migrations

Once the containers are up, apply the database migrations:

```sh
docker-compose exec web python manage.py migrate
```

### Create a Superuser

Create a superuser to access the Django admin interface:

```sh
docker-compose exec web python manage.py createsuperuser
```

### Collect Static Files

Collect static files for the application:

```sh
docker-compose exec web python manage.py collectstatic
```

## Running the Application

The application will be available at `http://localhost:8000`.

- Admin interface: `http://localhost:8000/admin`
- API endpoints:
  - Authentication: `http://localhost:8000/auth/`
  - Stock images: `http://localhost:8000/api/`

## Accessing the Deployed Version

The deployed version of the application can be accessed at [https://imagestock-backend.onrender.com](https://imagestock-backend.onrender.com).

## API Endpoints

### Authentication

- `POST /auth/register/` - Register a new user
- `POST /auth/verification/` - Verify user email
- `POST /auth/login/` - Login user
- `POST /auth/forgot-password/` - Request password reset
- `PATCH /auth/set-password/` - Set new password

### Stock Images

- `GET /api/images/` - List all images for the authenticated user
- `POST /api/images/` - Upload new images
- `PATCH /api/images/reorder/` - Reorder images
- `PATCH /api/images/<id>/` - Update image details
- `DELETE /api/images/<id>/` - Delete an image

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
