-- Create telemetry records table
CREATE TABLE IF NOT EXISTS telemetry (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER,
    value FLOAT,
    status VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Main BRIN index for BETWEEN queries by timestamp
CREATE INDEX idx_telemetry_timestamp_brin ON telemetry 
USING brin (timestamp) WITH (pages_per_range = 32);

-- Index to filter by sensor_id (B-Tree because the exact matches)
CREATE INDEX idx_telemetry_sensor_id ON telemetry (sensor_id);

-- Index for the regular queries by sensor_id + timestamp
CREATE INDEX idx_telemetry_sensor_timestamp ON telemetry (sensor_id, timestamp);
