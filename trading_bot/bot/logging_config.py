"""
Logging Configuration Module

This module sets up a structured logging system for the trading bot.
It routes log messages to both the console and a rotating log file.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Union

def setup_logger(name: str, level: Union[int, str] = logging.INFO) -> logging.Logger:
    """
    Set up and return a configured logger instance with console and file handlers.

    This function ensures that the log directory exists, configures log rotation,
    applies formatting, and prevents duplicate log handler registration.

    :param name: Name of the logger (typically the module name).
    :param level: Logging level for the logger and handlers (defaults to INFO).
    :return: A configured logging.Logger instance.
    """
    # Define and create the logs directory dynamically relative to this file
    bot_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(bot_dir)
    log_dir = os.path.join(project_root, 'logs')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'trading.log')

    # Get or create the logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Disable propagation to prevent double logging to the root logger
    logger.propagate = False

    # Prevent duplicate handlers if the logger was already initialized
    if logger.hasHandlers():
        logger.handlers.clear()

    # Define the log message format
    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(log_format, datefmt=date_format)

    # 1. Console Handler (Outputting to stdout/stderr)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. Rotating File Handler (Max 5MB, keep 5 backup files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
