# README

This project is a simple API built using FastAPI, with MongoDB as the database and JWT for authentication and authorization. It includes basic CRUD (Create, Read, Update, Delete) operations for an item model with `id` and `name` fields, as well as user authentication to protect certain endpoints. The project is set up to run on Windows Subsystem for Linux (WSL) and uses Poetry for dependency management. A Makefile is included to simplify common tasks.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Windows Subsystem for Linux (WSL):** Follow the [official guide](https://docs.microsoft.com/en-us/windows/wsl/install) to install WSL if you haven't done so already.
- **Python:** Ensure Python 3.8 or higher is installed on your WSL environment. You can check your version by running:

  ```bash
  python3 --version
  ```

- **Poetry:** Poetry is used for dependency management. Install Poetry by running the following command in your WSL terminal:

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

- **Docker:** Install Docker to run the MongoDB container. Follow the [official guide](https://docs.docker.com/get-docker/) if you need help.

## Project Structure

The project is organized into folders to keep the codebase clean and maintainable. The main components are:

```
your-project-name/
│
├── app/
│   ├── core/
│   │   ├── mongo_client.py        # MongoDB client using the Singleton pattern
│   │   └── security.py            # Security utilities for JWT
│   ├── main.py                    # The main FastAPI application file
│   ├── routers/
│   │   ├── items.py               # The router for item-related endpoints
│   │   ├── users.py               # The router for user-related endpoints (authentication, registration)
│   ├── models/
│   │   ├── item.py                # The item model definition
│   │   ├── user.py                # The user model definition
│   ├── repositories/
│   │   ├── mongo/
│   │   │   ├── base_mongo_repository.py  # Base repository with MongoDB operations
│   │   ├── item_mongo_repository.py  # Repository for Item model
│   │   └── user_mongo_repository.py  # Repository for User model
│   ├── services/
│   │   ├── user_service.py        # Business logic for user operations
│   └── utils/
│       └── password.py            # Password utilities for hashing and validation
│
├── Makefile                       # Makefile for easy commands
├── pyproject.toml                 # Poetry configuration file
└── README.md                      # Project documentation
```

### MongoDB Integration

This project uses MongoDB as the database, running inside a Docker container. The database operations are handled by repository classes to abstract database logic from the rest of the application.

### JWT Authentication

#### Objective

- Understand JWT (JSON Web Tokens) basics.
- Implement user authentication with JWT.
- Add authorization logic to the update and delete endpoints.
- Use the `pwdlib` library to encrypt user passwords.

#### New User Data Type

A new data type, `User`, is introduced with the following attributes:

- `_id`
- `name`
- `email` (using `pydantic[email]` for email type validation)
- `password`

The user data type includes models, repositories, services, and routers to handle user-related operations.

### 1. Setting Up MongoDB with Docker

Run the following command to start a MongoDB container:

```bash
docker run -d --name mongodb-container -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=pass mongo:latest
```

This will start a MongoDB instance accessible at `mongodb://localhost:27017`.

### 2. MongoDB Client

The MongoDB client is implemented using the Singleton pattern to ensure that only one instance of the client is created. The client is located in `app/core/mongo_client.py`.

### 3. Repository Pattern

The repository pattern is used to handle database operations in a clean and organized manner.

- **Base Mongo Repository:** `app/repositories/mongo/base_mongo_repository.py` contains the basic CRUD operations implemented for MongoDB.
- **Item Repository:** `app/repositories/item_mongo_repository.py` implements item-specific operations.
- **User Repository:** `app/repositories/user_mongo_repository.py` implements user-specific operations.

### 4. Security Utilities

`app/core/security.py` handles JWT token creation and user authentication. It includes functions for generating tokens and verifying user credentials during login.

#### Example Code for JWT Token Creation:

```python
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### 5. Password Utilities

`app/utils/password.py` includes functions for hashing and validating passwords using `pwdlib`.

Example functions:

```python
from pwdlib import argon2

def hash_password(password: str) -> str:
    return argon2.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return argon2.verify(plain_password, hashed_password)
```

### 6. Protecting Routes with JWT

Certain endpoints, such as user update and delete operations, require JWT authentication. Users can only edit their own records, and not those of others.

#### Example Protected Route:

In `app/routers/users.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user

router = APIRouter()

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: UserUpdate, current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    # Logic to update the user
```

### 7. Using MongoDB Compass

To view and manage the data saved in MongoDB, you can use MongoDB Compass, a GUI for MongoDB. Follow these steps:

1. [Download MongoDB Compass](https://www.mongodb.com/products/compass) and install it.
2. Open MongoDB Compass and connect to your MongoDB instance using the connection string `mongodb://localhost:27017`.
3. Navigate through the collections to view, insert, update, and delete documents.

## Project Setup

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/karenjunqueira/seed-backend-python
cd seed-backend-python
```

### 2. Install Dependencies

Use Poetry to install the required dependencies:

```bash
poetry install
```

### 3. Running the Application

You can use the included Makefile to easily run the application. The following commands are available:

- **Run the application:**

  ```bash
  make run-dev
  ```

  This will start the FastAPI server at `http://localhost:8000`.

### 4. Using the API

Once the server is running, you can interact with the API using HTTP methods like GET, POST, PUT, and DELETE. Here's a brief overview of the endpoints:

- **GET /items:** Retrieve a list of items.
- **GET /items/{id}:** Retrieve the item with the specified `id`.
- **POST /items:** Create a new item by providing an `id` and `name`.
- **PUT /items/{id}:** Update the item with the specified `id` (requires authentication).
- **DELETE /items/{id}:** Delete the item with the specified `id`.
- **POST /users:** Create a new user with `name`, `email`, and `password`.
- **POST /auth/token:** Authenticate a user and receive a JWT token.


## Makefile

The Makefile contains several useful commands:

```makefile
# Install dependencies
install:
	poetry install

# Run the application
run:
	fastapi dev app/main.py

```