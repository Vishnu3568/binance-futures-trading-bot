# Binance Futures Trading Bot

A modular, clean Python architecture skeleton for placing Market and Limit orders on Binance Futures Testnet (USDT-M).

## Project Overview
This repository provides a modular skeleton for a simplified algorithmic trading bot targeting the Binance USDT-M Futures exchange. It separates the API client layer, order manager service, input validation rules, logging configurations, and CLI entry point.

## Features
- **USDT-M Futures Trading**: Designed for placing MARKET and LIMIT orders.
- **Bi-directional Support**: Supports both BUY (long) and SELL (short) directions.
- **Input Validation**: Clean and modular parameters verification prior to sending request payloads.
- **Structured Logging**: Pre-configured logging structure to record execution flows, API request-responses, and exception stack traces.

## Project Structure
```text
trading_bot/
│
├── bot/
│   ├── __init__.py          # Exports package modules
│   ├── client.py            # API client wrapper
│   ├── orders.py            # Order placement and formatting
│   ├── validators.py        # CLI input validators
│   └── logging_config.py    # Console/File logging setup
│
├── logs/                    # Folder containing log files (created dynamically)
│
├── cli.py                   # Command Line Interface (CLI) entry point
├── README.md                # Project documentation
├── requirements.txt         # Project package requirements
├── .gitignore               # Ignored files (logs, environment variables)
└── .env.example             # Configuration example template
```

## Installation
Instructions on how to set up the environment:
1. Clone the repository.
2. Initialize and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Configure environment variables:
1. Copy `.env.example` to a local `.env` file.
2. Fill in the keys:
   ```env
   BINANCE_API_KEY=your_api_key_here
   BINANCE_API_SECRET=your_api_secret_here
   BASE_URL=https://testnet.binancefuture.com
   ```

## Running
Examples of how to run the CLI once implemented:
- **MARKET Order**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  ```
- **LIMIT Order**:
  ```bash
  python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 50000
  ```

## Logging
The project implements a structured logging system using Python's built-in `logging` module.

### Log File Location
Logs are saved in the project root directory under the `logs/` folder in the following file:
- `trading_bot/logs/trading.log` (automatically created at runtime if the directory does not exist).

### Console Logging
- Output is written directly to stdout/stderr.
- Follows the structured format: `Timestamp | Log Level | Module Name | Message`
- Level configured: `INFO` (with `DEBUG` support for future expansions).

### File Logging
- Output is written to `trading.log`.
- Follows the structured format: `Timestamp | Log Level | Module Name | Message`
- Level configured: `INFO`.

### Log Rotation
To prevent storage build-up, log files rotate dynamically:
- **Maximum File Size**: 5 MB per file.
- **Backup Count**: Keeps up to 5 historical backup files (e.g., `trading.log.1`, `trading.log.2`, etc.).

## Future Improvements
- Implement order quantity/price rounders mapping exchange step-size and tick-size filters.
- Integrate Stop-Limit, Take-Profit, and Trailing Stop order executions.
- Enhance CLI input parsing using rich UX packages (e.g. click, typer).
