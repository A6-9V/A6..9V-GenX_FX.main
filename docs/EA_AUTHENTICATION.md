# EA HTTP Authentication Guide

## Overview

The Expert Advisor (EA) HTTP API endpoints now require API key authentication for improved security. This protects sensitive trading data and prevents unauthorized access to trading signals and account information.

## Security Improvements

### What Changed

**Before:**
- EA HTTP endpoints were completely open (no authentication)
- Anyone could access `/get_signal`, `/ea_info`, `/heartbeat`, etc.
- Risk of unauthorized trading signal access
- Risk of account data exposure

**After:**
- All EA HTTP endpoints require `X-API-Key` header
- API keys are validated against configured secrets
- Failed authentication attempts are logged
- Better audit trail for EA connections

### Protected Endpoints

The following endpoints now require authentication:

#### EA Client Endpoints
- `GET /get_signal` - Retrieve trading signals
- `POST /ea_info` - Register EA information  
- `POST /heartbeat` - Send heartbeat
- `POST /account_status` - Submit account status
- `POST /trade_result` - Report trade execution results

#### Admin Endpoints
- `GET /ea_status` - View all connected EAs
- `POST /send_signal` - Add signal to queue
- `GET /trade_results` - View trade execution history

#### Public Endpoint (No Auth Required)
- `GET /ping` - Health check (remains unauthenticated)

## Configuration

### Environment Variables

Add one of the following to your `.env` file:

**Option 1: Single API Key**
```bash
EA_API_KEY=your_secure_random_key_here
```

**Option 2: Multiple API Keys (for multiple EAs)**
```bash
EA_API_KEYS=key1_for_ea1,key2_for_ea2,key3_for_ea3
```

### Generating Secure API Keys

Use a strong random string (32+ characters):

**Python:**
```python
import secrets
api_key = secrets.token_urlsafe(32)
print(f"EA_API_KEY={api_key}")
```

**Bash/Linux:**
```bash
openssl rand -base64 32
```

**PowerShell:**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

## Usage

### MetaTrader EA Integration

Update your MetaTrader EA code to include the API key in HTTP requests:

#### MQL4/MQL5 Example

```mql4
// Store your API key
string ea_api_key = "your_api_key_here";  // Move to external parameter for security

// Function to add API key header
string headers = "X-API-Key: " + ea_api_key + "\r\n" +
                 "Content-Type: application/json\r\n";

// Example: Get signal with authentication
int WebRequest(
    "GET",
    "http://your-server.com/get_signal",
    headers,
    NULL,
    0,
    result,
    headers_out
);

// Example: Send EA info with authentication  
string json_data = "{\"type\":\"ea_info\",\"data\":{...}}";
char post_data[];
StringToCharArray(json_data, post_data);

int WebRequest(
    "POST",
    "http://your-server.com/ea_info",
    headers,
    5000,
    post_data,
    result,
    headers_out
);
```

### Python Client Example

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "http://your-server.com"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Get signal
response = requests.get(f"{BASE_URL}/get_signal", headers=headers)
if response.status_code == 200:
    signal = response.json()
    print(signal)
elif response.status_code == 401:
    print("Authentication failed: Missing API key")
elif response.status_code == 403:
    print("Authentication failed: Invalid API key")

# Send heartbeat
heartbeat_data = {
    "type": "heartbeat",
    "data": {
        "account": 12345,
        "magic_number": 54321,
        "status": "active",
        "positions": 2,
        "pending_orders": 1,
        "last_signal": "BUY_EURUSD"
    }
}

response = requests.post(
    f"{BASE_URL}/heartbeat",
    headers=headers,
    json=heartbeat_data
)
print(response.json())
```

### cURL Example

```bash
# Set your API key
API_KEY="your_api_key_here"
SERVER="http://your-server.com"

# Get signal
curl -X GET "$SERVER/get_signal" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json"

# Send heartbeat
curl -X POST "$SERVER/heartbeat" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "heartbeat",
    "data": {
      "account": 12345,
      "magic_number": 54321,
      "status": "active",
      "positions": 2
    }
  }'
```

## Error Responses

### 401 Unauthorized - Missing API Key
```json
{
  "detail": "Missing API key. Please provide X-API-Key header."
}
```

**Solution:** Include `X-API-Key` header in your request

### 403 Forbidden - Invalid API Key
```json
{
  "detail": "Invalid API key"
}
```

**Solution:** Check that your API key matches the configured `EA_API_KEY` or is in `EA_API_KEYS`

### 500 Internal Server Error - No Keys Configured
```json
{
  "detail": "Server configuration error. Contact administrator."
}
```

**Solution:** Server admin needs to set `EA_API_KEY` or `EA_API_KEYS` in environment

## Best Practices

### Security

1. **Use Strong Keys:** Generate random keys with 32+ characters
2. **Keep Keys Secret:** Never commit API keys to version control
3. **Use Environment Variables:** Store keys in `.env` file (not in code)
4. **Rotate Keys Regularly:** Change API keys periodically
5. **Use HTTPS:** Always use HTTPS in production (not HTTP)
6. **One Key Per EA:** Use separate keys for different EAs for better tracking

### Deployment

1. **Production:** Set keys via environment variables or secrets manager
2. **Development:** Use `.env` file (add to `.gitignore`)
3. **Docker:** Use Docker secrets or environment variables
4. **Cloud:** Use cloud provider's secret management (AWS Secrets Manager, Azure Key Vault, etc.)

### Monitoring

- Check logs for failed authentication attempts
- Monitor for unusual API usage patterns
- Revoke compromised keys immediately
- Keep audit trail of EA connections

## Migration Guide

### For Existing EA Deployments

1. **Update Server:**
   - Add `EA_API_KEY` to your `.env` file
   - Restart the API server
   - Verify `/ping` still works (no auth required)

2. **Update EA Code:**
   - Add API key to EA parameters or config
   - Update all HTTP requests to include `X-API-Key` header
   - Test with `/ping` first, then `/get_signal`

3. **Gradual Rollout:**
   - Deploy updated server
   - Update and test one EA at a time
   - Monitor logs for authentication errors

### Backward Compatibility

If you need temporary backward compatibility during migration:

1. Set `EA_API_KEY` to an empty string temporarily (not recommended)
2. Or keep old unauthenticated endpoints as legacy endpoints
3. Plan to remove backward compatibility after migration

## Troubleshooting

### EA Can't Connect

1. **Check API key configuration:**
   ```bash
   echo $EA_API_KEY
   ```

2. **Verify server is running:**
   ```bash
   curl http://your-server.com/ping
   ```

3. **Test authentication:**
   ```bash
   curl -H "X-API-Key: your_key" http://your-server.com/get_signal
   ```

4. **Check server logs:**
   ```bash
   tail -f /var/log/genx-trading/app.log
   ```

### Common Issues

**"Invalid API key" error:**
- Verify key matches exactly (no extra spaces)
- Check if using `EA_API_KEY` or `EA_API_KEYS`
- Ensure server has been restarted after config change

**"Missing API key" error:**
- Verify `X-API-Key` header is being sent
- Check header name spelling (case-sensitive)
- Ensure header value is not empty

## Support

For issues or questions:
1. Check server logs for detailed error messages
2. Verify API key configuration
3. Test with cURL or Python before updating EA code
4. Contact your system administrator if problems persist

## Security Reporting

If you discover a security vulnerability, please report it to the security team immediately. Do not create a public issue.
