"""
Order Placement Service Module

This module implements the OrderManager class responsible for validating,
executing, and normalizing MARKET and LIMIT orders placed on Binance Futures Testnet.
"""

from typing import Dict, Any, Union
from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceRequestException
from requests.exceptions import RequestException

from bot.client import BinanceFuturesClient
from bot.validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_limit_requirements
)
from bot.logging_config import setup_logger

# Initialize the module logger
logger = setup_logger("orders")

class OrderManager:
    """
    Manager class to handle validation, submission, and normalization of orders.
    Uses the provided BinanceFuturesClient instance to communicate with the API.
    """

    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize the OrderManager.

        :param client: Reusable BinanceFuturesClient client wrapper instance.
        """
        self.client = client

    def _normalize_response(self, raw_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize the raw Binance response dictionary to return a normalized subset.

        :param raw_response: The raw API response dictionary.
        :return: A clean dictionary with normalized fields.
        """
        # Convert values to correct Python types where necessary
        orig_qty = float(raw_response.get("origQty", 0.0)) if raw_response.get("origQty") is not None else 0.0
        exec_qty = float(raw_response.get("executedQty", 0.0)) if raw_response.get("executedQty") is not None else 0.0
        price = float(raw_response.get("price", 0.0)) if raw_response.get("price") is not None else 0.0

        avg_price_raw = raw_response.get("avgPrice")
        avg_price = None
        if avg_price_raw is not None:
            try:
                avg_price = float(avg_price_raw)
            except (ValueError, TypeError):
                pass

        transact_time = raw_response.get("updateTime") or raw_response.get("time") or raw_response.get("transactTime")

        normalized = {
            "orderId": raw_response.get("orderId"),
            "symbol": raw_response.get("symbol"),
            "side": raw_response.get("side"),
            "type": raw_response.get("type"),
            "status": raw_response.get("status"),
            "origQty": orig_qty,
            "executedQty": exec_qty,
            "price": price,
            "avgPrice": avg_price,
            "clientOrderId": raw_response.get("clientOrderId"),
            "transactTime": transact_time
        }
        return normalized

    def _execute_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to execute the order and handle all related API or network errors.

        :param params: Formatted dictionary of Binance Futures create_order parameters.
        :return: Standardized, clean normalized response dictionary.
        :raises ConnectionError: On network failures.
        :raises ValueError: On invalid inputs or business exceptions.
        :raises RuntimeError: On general or unexpected API execution errors.
        """
        symbol = params.get("symbol")
        side = params.get("side")
        order_type = params.get("type")
        qty = params.get("quantity")
        price = params.get("price")

        logger.info("Order request")

        try:
            # Call underlying python-binance client instance
            raw_response = self.client.get_client().futures_create_order(**params)
            
            logger.info("Order response received")
            logger.info("Order placed successfully")
            normalized = self._normalize_response(raw_response)
            return normalized

        except BinanceAPIException as e:
            err_msg = f"Binance API Error placing order: {e.message} (Code: {e.code})"
            logger.error(err_msg)
            raise RuntimeError(err_msg) from e
            
        except BinanceOrderException as e:
            err_msg = f"Binance Order validation error: {e}"
            logger.error(err_msg)
            raise ValueError(err_msg) from e
            
        except BinanceRequestException as e:
            err_msg = f"API Request failed: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
            
        except RequestException as e:
            err_msg = f"Network communication failure: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
            
        except Exception as e:
            err_msg = f"Unexpected order execution error: {e}"
            logger.error(err_msg)
            raise RuntimeError(err_msg) from e

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a MARKET order (BUY or SELL) on Binance Futures Testnet.

        :param symbol: Trading pair symbol (e.g. BTCUSDT).
        :param side: Order side (BUY or SELL).
        :param quantity: Trade quantity (float).
        :return: Standardized dictionary containing normalized order details.
        :raises ValueError: If input parameters validation fails.
        """
        # Validate inputs before making API calls
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_type = validate_order_type("MARKET")
        v_qty = validate_quantity(quantity)
        logger.info(f"Placing MARKET {v_side} order")

        params = {
            "symbol": v_symbol,
            "side": v_side,
            "type": v_type,
            "quantity": v_qty
        }
        return self._execute_order(params)

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Place a LIMIT order (BUY or SELL) on Binance Futures Testnet.

        :param symbol: Trading pair symbol (e.g. BTCUSDT).
        :param side: Order side (BUY or SELL).
        :param quantity: Trade quantity (float).
        :param price: Order price (float).
        :return: Standardized dictionary containing normalized order details.
        :raises ValueError: If input parameters validation fails.
        """
        # Validate inputs before making API calls
        v_symbol = validate_symbol(symbol)
        v_side = validate_side(side)
        v_type = validate_order_type("LIMIT")
        v_qty = validate_quantity(quantity)
        v_price = validate_price(price)
        validate_limit_requirements(v_type, v_price)
        logger.info(f"Placing LIMIT {v_side} order")

        params = {
            "symbol": v_symbol,
            "side": v_side,
            "type": v_type,
            "quantity": v_qty,
            "price": v_price,
            "timeInForce": "GTC"
        }
        return self._execute_order(params)

# Package initializer compatibility alias
BinanceFuturesOrderManager = OrderManager
