# README

This project is a simple API built using FastAPI, with MongoDB as the database. It includes basic CRUD (Create, Read, Update, Delete) operations for an item model with `id` and `name` fields. The project is set up to run on Windows Subsystem for Linux (WSL) and uses Poetry for dependency management. A Makefile is included to simplify common tasks.

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
│   │   └── mongo_client.py   # MongoDB client using the Singleton pattern
│   ├── main.py               # The main FastAPI application file
│   ├── routers/
│   │   ├── items.py          # The router for item-related endpoints
│   ├── models/
│   │   ├── __init__.py       # Makes 'models' a module
│   │   ├── item.py           # The item model definition
│   ├── repositories/
│   │   ├── mongo/
│   │   │   ├── base_mongo_repository.py  # Base repository with MongoDB operations
│   │   ├── item_mongo_repository.py  # Repository for Item model
│
├── Makefile                  # Makefile for easy commands
├── pyproject.toml            # Poetry configuration file
└── README.md                 # Project documentation
```

### Separating Routers

The routers for different API endpoints are separated into their own modules within the `routers` folder. This separation allows you to organize your code more effectively as your project grows.

For example, the `item_router.py` file in the `routers` folder contains all the endpoints related to the `Item` model.

### MongoDB Integration

This project uses MongoDB as the database, running inside a Docker container. The database operations are handled by repository classes to abstract database logic from the rest of the application.

### 1. Setting Up MongoDB with Docker

Run the following command to start a MongoDB container:

```bash
docker run -d --name mongodb-container -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=pass mongo:latest
```

This will start a MongoDB instance accessible at `mongodb://localhost:27017`.

### 2. MongoDB Client

The MongoDB client is implemented using the Singleton pattern to ensure that only one instance of the client is created. The client is located in `app/core/mongo_client.py`.

Example code:

```python
from pymongo import MongoClient

class MongoClientSingleton:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient("mongodb://localhost:27017")
        return cls._client

mongo_client = MongoClientSingleton.get_client()
```

### 3. Repository Pattern

The repository pattern is used to handle database operations in a clean and organized manner.

- **Base Mongo Repository:** `app/repositories/mongo/base_mongo_repository.py` contains the basic CRUD operations implemented for MongoDB.


- **Item Repository:** `app/repositories/item_mongo_repository.py` implements the item-specific operations.


### 4. Referencing Routers in `main.py`

To use the routers in the main application, you'll need to import them in the `main.py` file and include them in the FastAPI app. Here’s an example:

```python
from fastapi import FastAPI
from routers.item_router import router as item_router

app = FastAPI()

# Include the items router
app.include_router(item_router, 
    prefix="/items",
    tags=["Item"])

```
This setup ensures that all the routes defined in `item_router.py` are registered with the FastAPI application.

### 5. Using MongoDB Compass

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
- **PUT /items/{id}:** Update the item with the specified `id`.
- **DELETE /items/{id}:** Delete the item with the specified `id`.


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