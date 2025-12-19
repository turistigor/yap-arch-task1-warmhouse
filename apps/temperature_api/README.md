# Smart Home Sensor Management API

## Getting Started

### Option 1: Using Docker Compose (Recommended)

#### Prerequisites

- Docker and Docker Compose

#### Launch

The easiest way to start the application is to use Docker Compose:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8081


### Option 2: Using Docker Compose (Recommended)

#### Prerequisites

- vcpkg
- cmake
- ninja
- gcc (>= 13.0.0)

#### Launch

Install dependency (it may be need subdependencies):

```bash
vcpkg install drogon
```

Build and run the application:
```bash
make build
make run
```

Remove the application:
```bash
make clean
```

The API will be available at http://localhost:8081

## API Testing

A Postman collection is provided for testing the API. Import the `temperature-api.postman_collection.json` file into Postman to get started.

## API Endpoints

- `GET /` - Service information
- `GET /healthcheck` - Healthcheck
- `GET /temperature?location=<value>` - Temperature by location
- `GET /temperature/:id` - Temperature by sensor id
