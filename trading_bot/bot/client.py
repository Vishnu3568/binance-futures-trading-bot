"""
Binance Futures Testnet Client Wrapper Module

This module defines the BinanceFuturesClient class, which manages credentials loading,
initialization of the python-binance Client, and connectivity verification.
"""

import os
from typing import Dict, Any, Union
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from requests.exceptions import RequestException
from bot.logging_config import setup_logger

# Load environment variables
load_dotenv()

# Initialize the module logger
logger = setup_logger("client")

class BinanceFuturesClient:
    """
    A client wrapper class for the Binance Futures Testnet API.
    Manages client instantiation, credential validation, ping checks,
    and server time queries.
    """

    def __init__(self, api_key: str = None, api_secret: str = None, base_url: str = None):
        """
        Initialize the Binance Futures client.
        Loads credentials from .env if not provided.

        :raises ValueError: If required environment variables or credentials are missing.
        """
        logger.info("Initializing BinanceFuturesClient...")
        
        # Load and validate credentials
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.base_url = base_url or os.getenv("BASE_URL")

        logger.info("Loading environment configurations...")
        
        missing_vars = []
        if not self.api_key:
            missing_vars.append("BINANCE_API_KEY")
        if not self.api_secret:
            missing_vars.append("BINANCE_API_SECRET")
        if not self.base_url:
            missing_vars.append("BASE_URL")

        if missing_vars:
            err_msg = f"Missing required configuration variables: {', '.join(missing_vars)}"
            logger.error(err_msg)
            raise ValueError(err_msg)

        # Log loaded credentials safely (never log API Secret, mask API Key)
        masked_key = f"{self.api_key[:5]}...{self.api_key[-5:]}" if len(self.api_key) > 10 else "..."
        logger.info(f"Loaded credentials. API Key: {masked_key} | Base URL: {self.base_url}")

        # Ensure base URL ends with '/fapi' as required by python-binance
        api_url = self.base_url.rstrip('/')
        if not api_url.endswith('/fapi'):
            api_url += '/fapi'

        try:
            # Instantiate python-binance client (testnet=True triggers testnet defaults, but we override URL)
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True
            )
            # Override futures endpoint URL dynamically with the configured BASE_URL
            self.client.FUTURES_URL = api_url
            self.client.FUTURES_TESTNET_URL = api_url
            logger.info(f"python-binance Client initialized and configured to use custom BASE_URL: {api_url}")
            
        except Exception as e:
            err_msg = f"Failed to initialize python-binance Client: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e

    def get_client(self) -> Client:
        """
        Get the underlying python-binance Client instance.

        :return: python-binance Client object.
        """
        return self.client

    def ping(self) -> bool:
        """
        Verify API reachability.

        :return: True if the ping request was successful.
        :raises ConnectionError: If the server is unreachable or returned an error.
        """
        logger.info("Sending ping request to Binance Futures Testnet...")
        try:
            self.client.futures_ping()
            logger.info("Ping request successful.")
            return True
        except BinanceAPIException as e:
            err_msg = f"Ping failed - API Error: {e.message} (Code: {e.code})"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except BinanceRequestException as e:
            err_msg = f"Ping failed - Request Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except RequestException as e:
            err_msg = f"Ping failed - Network Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except Exception as e:
            err_msg = f"Ping failed - Unexpected Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e

    def get_server_time(self) -> int:
        """
        Get the current Binance server time.

        :return: Server timestamp in milliseconds.
        :raises ConnectionError: If fetching server time failed.
        """
        logger.info("Requesting Binance server time...")
        try:
            time_data = self.client.futures_time()
            server_time = int(time_data["serverTime"])
            logger.info(f"Server time retrieved successfully: {server_time}")
            return server_time
        except BinanceAPIException as e:
            err_msg = f"Failed to fetch server time - API Error: {e.message} (Code: {e.code})"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except RequestException as e:
            err_msg = f"Failed to fetch server time - Network Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except Exception as e:
            err_msg = f"Failed to fetch server time - Unexpected Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e

    def test_connection(self) -> bool:
        """
        Verify communication and validate credentials with Binance Futures Testnet.
        Executes a private authenticated query.

        :return: True if the connection and credentials validation succeeded.
        :raises PermissionError: If credentials signature/validation failed.
        :raises ConnectionError: If connection or API queries failed.
        """
        logger.info("Testing authenticated connection and verifying credentials...")
        try:
            # We call futures_account_balance() which is a lightweight authenticated call
            self.client.futures_account_balance()
            logger.info("Authenticated connection test successful. Credentials are valid.")
            return True
        except BinanceAPIException as e:
            # Specific handling for authentication failure codes (e.g. -1022 signature failed, -2015 invalid key)
            if e.code in (-1022, -2015, -1002):
                err_msg = f"Authentication test failed: {e.message} (Code: {e.code})"
                logger.error(err_msg)
                raise PermissionError(err_msg) from e
            else:
                err_msg = f"Connection test failed - API Error: {e.message} (Code: {e.code})"
                logger.error(err_msg)
                raise ConnectionError(err_msg) from e
        except RequestException as e:
            err_msg = f"Connection test failed - Network/Request Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
        except Exception as e:
            err_msg = f"Connection test failed - Unexpected Error: {e}"
            logger.error(err_msg)
            raise ConnectionError(err_msg) from e
