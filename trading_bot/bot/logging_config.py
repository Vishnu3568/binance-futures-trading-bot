"""
Logging Configuration Module

This module sets up and configures the application loggers.
It provides console and file loggers with custom formatting.
"""

def setup_logging(log_level="INFO"):
    """
    Configure and return loggers for the application.

    :param log_level: The logging level to set (e.g. INFO, DEBUG)
    """
    # TODO: Implement setup_logging function
    # 1. Create logs/ directory if it doesn't exist.
    # 2. Add RotatingFileHandler to write logs/bot.log at DEBUG level.
    # 3. Add StreamHandler to write to console at the specified log_level.
    # 4. Use custom formatters for request, response, and error tracing.
    pass
