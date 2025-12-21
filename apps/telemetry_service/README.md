# Smart Home Telemetry API

The service collects telemetry data from the temperature api service and provides some statistics. The service focuses on data, a set of registered devices provided by a monolith (smart_home).

**BE CAREFUL!** Currently, the service does not restrict the recording of telemetry in the database in any way. By default, recording is performed once per second for each registered device.

## Getting Started

### Option 1: Using Docker Compose (Recommended)

#### Prerequisites

- Docker and Docker Compose

The easiest way to start the application is to use Docker Compose:

```bash
docker-compose up -d
```

The API will be available at http://localhost:8082


### Option 2: Manual setup

If you prefer to run the application without Docker:

1. Start the PostgreSQL database:

```bash
docker-compose up -d tm-db
```

2. Start the smart-home service:

[Readme](../README.md)

3. Start the temperature-api  service:

[Readme](../temperature_api/README.md)

2. Build and run the application:

```bash
cd apps/telemetry_service
uv sync
uv run python3 -m telemetry
```

## API Testing

A Postman collection is provided for testing the API. Import the `telemetry-api.postman_collection.json` file into Postman to get started.

## API Endpoints

- `GET /health` - Health check
- `GET /api/v1/sensors` - Get all sensors
- `GET /api/v1/sensors/:id` - Get a specific sensor
- `POST /api/v1/sensors` - Create a new sensor
- `PUT /api/v1/sensors/:id` - Update a sensor
- `DELETE /api/v1/sensors/:id` - Delete a sensor
- `PATCH /api/v1/sensors/:id/value` - Update a sensor's value and status

- `GET /api/v1/healthcheck` - Healthcheck
- `GET /api/v1/stat/get_tm?sensor_id=<value>&start_time=<value>&end_time=<value>` - device (sensor_id) telemetry statistic
