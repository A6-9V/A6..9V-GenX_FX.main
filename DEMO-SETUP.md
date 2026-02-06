# EXNESS Demo Account Setup

**Last Updated**: 2025-12-29 13:22:20

## Demo Account Configuration

**Account Details:**
- Account Number: `279410452`
- Server: `Exness-MT5Trial8`
- Password: `Leng3A69V[@Una]`
- Type: Demo/Testing Account

## Trading Symbols Configured

### Major Forex Pairs (10 symbols)
1. **EURUSD** - Euro vs US Dollar
2. **GBPUSD** - British Pound vs US Dollar
3. **USDJPY** - US Dollar vs Japanese Yen
4. **AUDUSD** - Australian Dollar vs US Dollar
5. **USDCAD** - US Dollar vs Canadian Dollar
6. **NZDUSD** - New Zealand Dollar vs US Dollar
7. **EURGBP** - Euro vs British Pound
8. **EURJPY** - Euro vs Japanese Yen
9. **GBPJPY** - British Pound vs Japanese Yen
10. **USDCHF** - US Dollar vs Swiss Franc

### Precious Metals (2 symbols)
11. **XAUUSD** - Gold vs US Dollar
12. **XAGUSD** - Silver vs US Dollar

### Cryptocurrencies (2 symbols)
13. **BTCUSD** - Bitcoin vs US Dollar
14. **ETHUSD** - Ethereum vs US Dollar

### Indices (3 symbols)
15. **US30** - US 30 Index (Dow Jones)
16. **NAS100** - NASDAQ 100 Index
17. **SPX500** - S&P 500 Index

### Micro Accounts (3 symbols)
18. **EURUSDm** - Euro vs US Dollar (Micro)
19. **GBPUSDm** - British Pound vs US Dollar (Micro)
20. **USDJPYm** - US Dollar vs Japanese Yen (Micro)

**Total: 20 Trading Symbols**

## Configuration Files

### 1. `config/brokers.json`
- Contains demo account credentials
- Set as default broker: `EXNESS_DEMO`

### 2. `config/symbols.json`
- Contains all 20 trading symbols
- Risk management settings per symbol
- Lot size limits

### 3. `config/mt5-demo.json`
- MT5-specific configuration
- Trading settings (stop loss, take profit)
- Enabled symbols list

## How to Use

### 1. Connect MT5 to Demo Account

1. Open MetaTrader 5
2. Go to **File → Login to Trade Account**
3. Enter credentials:
   - **Login**: `279410452`
   - **Password**: `Leng3A69V[@Una]`
   - **Server**: `Exness-MT5Trial8`
4. Click **Login**

### 2. Verify Account Connection

- Check account balance (should show demo balance)
- Verify server shows: `Exness-MT5Trial8`
- Check account type shows: **Demo**

### 3. Connect EA to Docker Bridge

1. Attach your EA (e.g., `PythonBridgeEA`) to a chart
2. Configure EA parameters:
   - **BridgePort**: `5555`
   - **BrokerName**: `EXNESS_DEMO`
   - **AutoExecute**: `true`
   - **Symbol**: Select from configured symbols
3. Check EA logs in MT5 (View → Terminal → Experts tab)

### 4. Start Docker Services

```powershell
cd exness-docker
docker-compose up -d
```

### 5. Verify Bridge Connection

- Check API health: http://localhost:8000/health
- Check EA logs in MT5 for connection status
- Verify symbols are available in MT5 Market Watch

## Trading Settings

**Default Risk Management:**
- Risk per trade: 1.0%
- Max positions per symbol: 1
- Min lot size: 0.01
- Max lot size: 10.0
- Default stop loss: 50 pips
- Default take profit: 100 pips

**Symbol-Specific Settings:**
- Major pairs: 1.0% risk
- Cryptocurrencies: 0.5% risk (higher volatility)
- All symbols: Same lot size limits

## Testing Checklist

- [ ] MT5 connected to demo account
- [ ] Account shows demo balance
- [ ] Server: Exness-MT5Trial8
- [ ] Docker services running
- [ ] Bridge API accessible (port 8000)
- [ ] EA attached and connected to bridge (port 5555)
- [ ] Symbols visible in Market Watch
- [ ] Test order placed successfully
- [ ] Orders visible in MT5 Terminal

## Important Notes

1. **Demo Account Only**: This is a testing account - no real money
2. **Symbol Availability**: Not all symbols may be available on demo server
3. **Market Hours**: Some symbols trade 24/5, cryptocurrencies trade 24/7
4. **Lot Sizes**: Verify minimum/maximum lot sizes per symbol in MT5
5. **Spread**: Demo accounts may have different spreads than live accounts

## Troubleshooting

### Account Login Failed
- Verify server name: `Exness-MT5Trial8` (case-sensitive)
- Check password: `Leng3A69V[@Una]` (includes special characters)
- Ensure MT5 is updated to latest version

### Symbol Not Found
- Some symbols may not be available on demo server
- Check Market Watch in MT5
- Verify symbol name matches exactly (case-sensitive)

### Bridge Connection Failed
- Ensure Docker services are running: `docker-compose ps`
- Check bridge port 5555 is not blocked by firewall
- Verify EA parameter: `BridgePort = 5555`

### EA Not Executing
- Check EA is enabled (green smiley face in chart)
- Verify AutoExecute parameter is set to `true`
- Check EA logs for error messages
- Ensure account has sufficient demo balance

## Next Steps

1. **Test Trading**: Place small test orders on demo account
2. **Monitor Performance**: Use Grafana dashboard (http://localhost:3000)
3. **Review Logs**: Check Docker logs: `docker-compose logs -f trading-bridge`
4. **Adjust Settings**: Modify risk parameters in `config/symbols.json` as needed

---

**Remember**: This is a demo account for testing only. Always test thoroughly before using real money.

