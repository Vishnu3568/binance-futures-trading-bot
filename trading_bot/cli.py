"""
Command Line Interface Entry Point

This script serves as the CLI command parser for the trading bot.
It reads arguments from the terminal, validates them, and invokes
the order placement manager.
"""

import sys
import argparse
from typing import Optional, Dict, Any
from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceRequestException

from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import validate_order_inputs

def main() -> None:
    """
    Main CLI parsing, validation, and execution entry point.
    """
    # Force UTF-8 encoding on standard output to support printing check/cross marks on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    # 1. Parse CLI arguments
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")
    
    parser.add_argument("--symbol", required=True, type=str, help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True, type=str, help="Order side (BUY or SELL)")
    parser.add_argument("--type", required=True, type=str, help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", required=True, type=float, help="Trade quantity")
    parser.add_argument("--price", required=False, type=float, default=None, help="Price (required for LIMIT orders)")
    
    args = parser.parse_args()

    # 2. Validate parsed inputs using validators
    try:
        validated = validate_order_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
    except ValueError as e:
        print(f"Validation Error: {e}")
        print("✗ Order failed")
        sys.exit(1)

    # 3. Print formatted request summary
    print("----------------------------------------")
    print("Order Request")
    print("----------------------------------------")
    print(f"Symbol : {validated['symbol']}")
    print(f"Side : {validated['side']}")
    print(f"Type : {validated['type']}")
    print(f"Quantity : {validated['quantity']}")
    if validated['type'] == 'LIMIT':
        print(f"Price : {validated['price']}")
    print("----------------------------------------")

    # 4. Initialize client and manager and place order
    try:
        client = BinanceFuturesClient()
        manager = OrderManager(client)

        if validated['type'] == 'LIMIT':
            response = manager.place_limit_order(
                symbol=validated['symbol'],
                side=validated['side'],
                quantity=validated['quantity'],
                price=validated['price']
            )
        else:
            response = manager.place_market_order(
                symbol=validated['symbol'],
                side=validated['side'],
                quantity=validated['quantity']
            )

        # 5. Print formatted response summary
        print("----------------------------------------")
        print("Order Response")
        print("----------------------------------------")
        print(f"Order ID : {response['orderId']}")
        print(f"Status : {response['status']}")
        print(f"Executed Qty : {response['executedQty']}")
        print(f"Price : {response['price']}")
        
        avg_price = response.get("avgPrice")
        avg_price_str = str(avg_price) if avg_price is not None else "N/A"
        print(f"Average Price : {avg_price_str}")
        print(f"Client Order ID : {response['clientOrderId']}")
        print("----------------------------------------")

        # 6. Success confirmation
        print("✓ Order placed successfully")

    except PermissionError as e:
        print(f"Permission Error: {e}")
        print("✗ Order failed")
        sys.exit(1)
    except ConnectionError as e:
        print(f"Connection Error: {e}")
        print("✗ Order failed")
        sys.exit(1)
    except ValueError as e:
        print(f"Value Error: {e}")
        print("✗ Order failed")
        sys.exit(1)
    except BinanceAPIException as e:
        print(f"Binance API Error: {e.message} (Code: {e.code})")
        print("✗ Order failed")
        sys.exit(1)
    except BinanceOrderException as e:
        print(f"Binance Order Error: {e}")
        print("✗ Order failed")
        sys.exit(1)
    except BinanceRequestException as e:
        print(f"Binance Request Error: {e}")
        print("✗ Order failed")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print("✗ Order failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
