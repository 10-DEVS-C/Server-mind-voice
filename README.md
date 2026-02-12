# Modular Flask API Base

This is a production-ready, modular Flask API base with MongoDB, JWT Authentication, and Swagger documentation.

## Features

- **Modular Structure**: Logic separated into modules (`auth`, `users`, etc.).
- **MongoDB**: Native integration via `flask-pymongo`.
- **Authentication**: JWT-based auth with `flask-jwt-extended`.
- **Validation**: Request/Response validation using `marshmallow` schemas.
- **Documentation**: Auto-generated Swagger UI via `flask-smorest`.
- **Security**: Rate limiting, CORS, and secure headers.
- **Base Classes**: Generic Service and Controller patterns for CRUD.
- **Microservices Ready**: Designed to be extended into microservices.

## ID Handling
All IDs (Primary Keys and Foreign Keys) are handled as **MongoDB ObjectIds** (24-character hex strings).
- **Frontend**: Should send and receive IDs as strings.
- **Backend**: Automatically validates and converts strings to `bson.ObjectId` in the Service layer.
- **Database**: Stores them as native `ObjectId` for performance and consistency.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    -   Copy `.env.example` to `.env` (if available) or create one.
    -   Set `FLASK_ENV` to `development` or `production`.
    -   Set `MONGO_URI` and `JWT_SECRET_KEY` in your environment variables.
    -   Default Mongo URI: `mongodb://localhost:27017/mind_voice_db`

3.  **Run the Application**:
    ```bash
    python run.py
    ```

4.  **Access Documentation**:
    Open your browser and navigate to:
    [http://localhost:5000/swagger-ui](http://localhost:5000/swagger-ui)

## Project Structure

```
app/
├── configs/          # Configuration files (dev, prod)
├── core/             # Base classes (Service, Utils)
├── middlewares/      # Error handling, Auth hooks
├── modules/          # Feature modules (Auth, Users)
├── extensions.py     # Flask extensions (Mongo, JWT, etc.)
└── __init__.py       # App factory
run.py                # Entry point
```

## Creating a New Module

1.  Create a folder in `app/modules/`.
2.  Create `models.py`, `schemas.py`, `services.py`, `controllers.py`.
3.  Inherit user service from `BaseService` in `services.py`.
4.  Define Schemas in `schemas.py`.
5.  Create a Blueprint in `controllers.py` and register routes.
6.  Register the blueprint in `app/__init__.py`.
