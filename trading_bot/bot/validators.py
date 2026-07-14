"""
Input Validators Module

This module contains validator functions to sanitize and validate
user inputs received from the command-line interface.
"""

from typing import Any, Dict

def validate_symbol(symbol: str) -> str:
    """
    Validate and format the trading symbol.

    Removes leading/trailing whitespace, converts to uppercase, and rejects
    empty values, symbols containing spaces, or non-string inputs.

    :param symbol: The trading symbol string (e.g. 'BTCUSDT').
    :return: Sanitized and uppercase symbol.
    :raises ValueError: If validation fails.
    """
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string.")
        
    sanitized = symbol.strip().upper()
    
    if not sanitized:
        raise ValueError("Symbol cannot be empty.")
        
    if " " in sanitized:
        raise ValueError(f"Symbol '{symbol}' cannot contain spaces.")
        
    return sanitized

def validate_side(side: str) -> str:
    """
    Validate and format the order side (BUY or SELL).

    :param side: The order side.
    :return: Upper-cased validated side.
    :raises ValueError: If the side is invalid.
    """
    if not isinstance(side, str):
        raise ValueError("Order side must be a string.")
        
    sanitized = side.strip().upper()
    if sanitized not in ("BUY", "SELL"):
        raise ValueError(f"Invalid order side: '{side}'. Allowed values are BUY, SELL.")
        
    return sanitized

def validate_order_type(order_type: str) -> str:
    """
    Validate and format the order type (MARKET or LIMIT).

    :param order_type: The order type.
    :return: Upper-cased validated order type.
    :raises ValueError: If the order type is invalid.
    """
    if not isinstance(order_type, str):
        raise ValueError("Order type must be a string.")
        
    sanitized = order_type.strip().upper()
    if sanitized not in ("MARKET", "LIMIT"):
        raise ValueError(f"Invalid order type: '{order_type}'. Allowed values are MARKET, LIMIT.")
        
    return sanitized

def validate_quantity(quantity: Any) -> float:
    """
    Validate and convert quantity to a float.

    Quantity must be a positive float greater than zero.

    :param quantity: The trade quantity (string, int, or float).
    :return: Float value of the quantity.
    :raises ValueError: If conversion fails or quantity is <= 0.
    """
    try:
        val = float(quantity)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Quantity must be a valid number, got: '{quantity}'") from e
        
    if val <= 0:
        raise ValueError(f"Quantity must be greater than zero, got: {val}")
        
    return val

def validate_price(price: Any) -> float:
    """
    Validate and convert price to a float.

    Price must be a positive float greater than zero.

    :param price: The trade price (string, int, or float).
    :return: Float value of the price.
    :raises ValueError: If conversion fails or price is <= 0.
    """
    if price is None:
        raise ValueError("Price is required.")
        
    try:
        val = float(price)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Price must be a valid number, got: '{price}'") from e
        
    if val <= 0:
        raise ValueError(f"Price must be greater than zero, got: {val}")
        
    return val

def validate_limit_requirements(order_type: str, price: Any) -> None:
    """
    Ensure limit order parameters are present.

    If the order type is LIMIT, the price must not be None.
    If the order type is MARKET, the price is ignored.

    :param order_type: The validated order type (LIMIT or MARKET).
    :param price: The price value.
    :raises ValueError: If order type is LIMIT but price is missing/None.
    """
    if order_type.strip().upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")

def validate_order_inputs(symbol: str, side: str, order_type: str, quantity: Any, price: Any = None) -> Dict[str, Any]:
    """
    Helper function to validate and format all order inputs together.

    :param symbol: Trading symbol.
    :param side: Side (BUY/SELL).
    :param order_type: Type (MARKET/LIMIT).
    :param quantity: Trade quantity.
    :param price: Trade price (optional for MARKET).
    :return: Dictionary containing all validated and formatted parameters.
    """
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_type = validate_order_type(order_type)
    clean_qty = validate_quantity(quantity)
    
    validate_limit_requirements(clean_type, price)
    
    clean_price = None
    if clean_type == "LIMIT":
        clean_price = validate_price(price)
        
    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "type": clean_type,
        "quantity": clean_qty,
        "price": clean_price
    }

def validate_inputs(symbol: str, side: str, order_type: str, quantity: Any, price: Any = None) -> Dict[str, Any]:
    """
    Validation entry point to maintain compatibility with bot package initializers.
    """
    return validate_order_inputs(symbol, side, order_type, quantity, price)
