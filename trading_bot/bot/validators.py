"""
Input Validators Module

This module contains validator functions to sanitize and validate
user inputs received from the command-line interface.
"""

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
    """
    Validate CLI parameters for MARKET and LIMIT orders.

    :param symbol: Trading symbol (e.g. BTCUSDT)
    :param side: BUY or SELL side
    :param order_type: MARKET or LIMIT type
    :param quantity: Trade quantity
    :param price: Price (required for LIMIT orders)
    :return: A dictionary of cleaned/validated values
    :raises ValueError: If any input fails validation
    """
    # TODO: Implement parameter validations
    # 1. Verify symbol is a non-empty string and conforms to standard formats (e.g., uppercase).
    # 2. Verify side is either BUY or SELL.
    # 3. Verify order_type is either MARKET or LIMIT.
    # 4. Verify quantity is a positive number.
    # 5. Verify price is a positive number when order_type is LIMIT.
    # 6. Verify environment configurations (credentials presence).
    pass
