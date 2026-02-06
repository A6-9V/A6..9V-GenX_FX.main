# Configuration Guide

## Environment Variables

All configuration is managed through environment variables in the `.env` file.

### Quick Setup

1. Copy the template:
   ```powershell
   Copy-Item env.template .env
   # Or use the setup script:
   .\scripts\setup-env.ps1
   ```

2. Edit `.env` with your values:
   ```powershell
   notepad .env
   ```

3. Start services:
   ```powershell
   docker-compose up -d
   ```

## Configuration Sections

### EXNESS Account Configuration

```env
EXNESS_LOGIN=your_account_number_here
EXNESS_PASSWORD=your_password_here
EXNESS_SERVER=your_server_name_here
EXNESS_IS_DEMO=true
```

**Description**:
- `EXNESS_LOGIN`: Your MT5 account number
- `EXNESS_PASSWORD`: Your MT5 account password
- `EXNESS_SERVER`: MT5 server name
- `EXNESS_IS_DEMO`: Set to `true` for demo accounts

### MT5 Terminal Configuration

```env
MT5_PATH=C:\Users\USER\AppData\Roaming\MetaQuotes\Terminal\53785E099C927DB68A545C249CDBCE06
MT5_TERMINAL_PATH=/mt5
```

**Description**:
- `MT5_PATH`: Windows path to MT5 terminal directory
- `MT5_TERMINAL_PATH`: Mounted path inside Docker container

### Trading Bridge Configuration

```env
BRIDGE_PORT=5555
API_PORT=8000
LOG_LEVEL=INFO
```

**Description**:
- `BRIDGE_PORT`: Port for MT5 EA connections (default: 5555)
- `API_PORT`: Port for REST API (default: 8000)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Trading Symbols Configuration

#### Method 1: Environment Variable (Simple List)

```env
SYMBOLS=EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD,NZDUSD
```

**Description**: Comma-separated list of symbols. Uses default settings (1% risk, 0.01-10.0 lot size).

#### Method 2: JSON Configuration (Detailed Settings)

Edit `config/symbols.json` for detailed per-symbol settings:
- Risk percentage
- Lot size limits
- Max positions
- Custom descriptions

#### Method 3: Hybrid (Recommended)

Use both:
- `SYMBOLS` env var for quick symbol list
- `config/symbols.json` for detailed settings
- Bridge service merges both automatically

**Example**:
```env
SYMBOLS=EURUSD,GBPUSD,USDJPY,EURCAD,EURCHF,EURAUD
```

Symbols in JSON get detailed settings, others use defaults.

### Database Configuration

#### PostgreSQL

```env
POSTGRES_DB=exness_trading
POSTGRES_USER=exness_user
POSTGRES_PASSWORD=exness_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

#### Redis

```env
REDIS_HOST=redis
REDIS_PORT=6379
```

#### InfluxDB

```env
INFLUXDB_URL=http://influxdb:8086
INFLUXDB_ORG=exness
INFLUXDB_BUCKET=trading_data
INFLUXDB_ADMIN_USER=admin
INFLUXDB_ADMIN_PASSWORD=adminpassword
```

#### Grafana

```env
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

## Configuration Files

### config/symbols.json

Detailed symbol configuration with risk management:

```json
{
  "symbols": [
    {
      "symbol": "EURUSD",
      "broker": "EXNESS_DEMO",
      "enabled": true,
      "risk_percent": 1.0,
      "max_positions": 1,
      "min_lot_size": 0.01,
      "max_lot_size": 10.0,
      "description": "Euro vs US Dollar"
    }
  ]
}
```

### config/brokers.json

Broker configuration:

```json
{
  "brokers": [
    {
      "name": "EXNESS_DEMO",
      "type": "demo",
      "server": "Exness-MT5Trial8",
      "account_id": "279410452",
      "enabled": true
    }
  ],
  "default_broker": "EXNESS_DEMO"
}
```

## Configuration Priority

1. **Environment Variables** (`.env` file) - Highest priority
2. **JSON Configuration Files** (`config/*.json`) - Detailed settings
3. **Default Values** - Fallback if not specified

## Validation

Configuration is validated on service startup:
- Missing required variables → Service fails to start
- Invalid paths → Warning logged, service continues
- Invalid symbols → Default settings applied

## Security Best Practices

1. **Never commit `.env` file** to version control
2. **Use strong passwords** for database services
3. **Restrict network access** to exposed ports
4. **Regularly rotate credentials**
5. **Use secrets management** in production

## Troubleshooting

### Service won't start
- Check `.env` file exists
- Verify all required variables are set
- Check Docker logs: `docker-compose logs`

### Symbols not loading
- Verify `SYMBOLS` env var format (comma-separated)
- Check `config/symbols.json` syntax
- Review bridge service logs

### Connection issues
- Verify `MT5_PATH` is correct
- Check Docker Desktop file sharing settings
- Ensure MT5 terminal is running

---

**Last Updated**: 2025-12-29

