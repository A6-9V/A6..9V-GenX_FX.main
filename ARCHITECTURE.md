# EXNESS Docker Architecture

## System Overview

The EXNESS Docker setup provides a containerized trading infrastructure that connects to MetaTrader 5 (MT5) terminal running natively on Windows. The system bridges MT5 Expert Advisors (EAs) with supporting services for data storage, caching, and monitoring.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Windows Host System                       │
│                                                              │
│  ┌──────────────────┐         ┌──────────────────────┐    │
│  │  MetaTrader 5    │         │   Docker Desktop      │    │
│  │  Terminal        │◄────────┤                       │    │
│  │                  │  Port   │  ┌─────────────────┐ │    │
│  │  Expert Advisor  │  5555    │  │ Trading Bridge  │ │    │
│  │  (PythonBridgeEA)│          │  │   Service       │ │    │
│  └──────────────────┘         │  │  (Python/FastAPI)│ │    │
│                                 │  └────────┬────────┘ │    │
│                                 │           │           │    │
│                                 │  ┌────────▼────────┐ │    │
│                                 │  │   PostgreSQL    │ │    │
│                                 │  │   (Trade DB)    │ │    │
│                                 │  └─────────────────┘ │    │
│                                 │                       │    │
│                                 │  ┌─────────────────┐ │    │
│                                 │  │     Redis       │ │    │
│                                 │  │    (Cache)      │ │    │
│                                 │  └─────────────────┘ │    │
│                                 │                       │    │
│                                 │  ┌─────────────────┐ │    │
│                                 │  │    InfluxDB     │ │    │
│                                 │  │  (Time-Series)  │ │    │
│                                 │  └────────┬────────┘ │    │
│                                 │           │           │    │
│                                 │  ┌────────▼────────┐ │    │
│                                 │  │    Grafana      │ │    │
│                                 │  │  (Dashboard)    │ │    │
│                                 │  └─────────────────┘ │    │
│                                 └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Trading Bridge Service
- **Technology**: Python 3.11, FastAPI, Socket Server
- **Purpose**: Connects MT5 EAs to Docker services
- **Ports**: 
  - 5555: Socket bridge for MT5 EA connections
  - 8000: REST API for health checks and monitoring
- **Features**:
  - Hybrid symbols configuration (env var + JSON)
  - Environment variable-based configuration
  - Health check endpoints
  - MT5 path validation

### 2. PostgreSQL Database
- **Image**: postgres:15-alpine
- **Purpose**: Store trade history, positions, and trading data
- **Port**: 5432
- **Data Persistence**: Docker volume `postgres-data`

### 3. Redis Cache
- **Image**: redis:7-alpine
- **Purpose**: Real-time data caching and pub/sub messaging
- **Port**: 6379
- **Data Persistence**: Docker volume `redis-data`

### 4. InfluxDB
- **Image**: influxdb:2.7-alpine
- **Purpose**: Time-series metrics storage for trading analytics
- **Port**: 8086
- **Data Persistence**: Docker volumes `influxdb-data`, `influxdb-config`

### 5. Grafana
- **Image**: grafana/grafana:latest
- **Purpose**: Monitoring dashboards and visualization
- **Port**: 3000
- **Data Persistence**: Docker volume `grafana-data`
- **Data Sources**: InfluxDB

## Data Flow

### Trading Flow
1. MT5 EA sends trading signal → Bridge (port 5555)
2. Bridge validates and processes → Stores in PostgreSQL
3. Real-time updates → Redis cache
4. Metrics collection → InfluxDB
5. Visualization → Grafana dashboard

### Configuration Flow
1. Environment variables loaded from `.env` file
2. Symbols merged from `SYMBOLS` env var and `config/symbols.json`
3. Bridge service reads configuration on startup
4. All services use environment variables for configuration

## Network Architecture

- **Network**: `exness-network` (bridge driver)
- **Isolation**: All services communicate within Docker network
- **External Access**: Only exposed ports (5555, 8000, 3000, 5432, 6379, 8086)
- **MT5 Integration**: Volume mount from Windows host to container

## Security Considerations

- **Credentials**: Stored in `.env` file (git-ignored)
- **Network**: Services isolated in Docker network
- **Volume Mounts**: Read-only mount for MT5 terminal directory
- **Health Checks**: All services have health check endpoints
- **Restart Policies**: `unless-stopped` for automatic recovery

## Scalability

- **Horizontal Scaling**: Bridge service can be scaled (with session management)
- **Database**: PostgreSQL supports connection pooling
- **Cache**: Redis supports clustering
- **Monitoring**: Grafana can handle multiple data sources

## Dependencies

```
trading-bridge
  ├── depends_on: postgres (healthy), redis (started)
  └── healthcheck: HTTP /health endpoint

grafana
  └── depends_on: influxdb (healthy)

All services
  └── network: exness-network
```

## Configuration Management

- **Environment Variables**: Primary configuration method
- **JSON Configs**: Detailed settings (symbols, brokers)
- **Hybrid Approach**: Merge env vars with JSON for flexibility
- **Validation**: Configuration validated on service startup

## Monitoring & Health

- **Health Checks**: All services have health check endpoints
- **Logging**: Centralized logging to `logs/` directory
- **Metrics**: Time-series data in InfluxDB
- **Dashboards**: Grafana for visualization

---

**Last Updated**: 2025-12-29

