"""
Module for configuring and managing logging functionality.
This module provides utilities for setting up logging in Python applications,
with a focus on consistent formatting and console output. It includes functions
for creating and configuring loggers with standardized formatting.
  >> > from utils.logger import configure_logger
  >> > logger = configure_logger("my_app")
Attributes:
  No module level attributes.
Dependencies:
  - logging: Python's built-in logging module"""
import logging


def configure_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger with specific formatting and handling.
    This function creates or retrieves a logger with the specified name and configures it
    with a StreamHandler that outputs to standard output (console). The logger is set up
    with a specific format and INFO level logging.
    Args:
      name (str): The name to be used for the logger.
    Returns:
      logging.Logger: A configured logger instance that will output formatted messages
      to the console at INFO level or above.
    Example:
      >>> logger = configure_logger("my_application")
      >>> logger.info("Application started")
      2023-12-20 10:30:45,123 - my_application - INFO - Application started
    """

    # Obtiene un logger con el nombre especificado. Si ya existe, lo devuelve; si no, lo crea.
    logger = logging.getLogger(name)
    # Envía los mensajes de registro a la salida estándar (como la consola).
    handler = logging.StreamHandler()
    # Establece el nivel de registro del logger.
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Aplica el formato definido al handler.
    handler.setFormatter(formatter)
    # El logger usará este handler para procesar los mensajes.
    logger.addHandler(handler)
    # Configura el logger para que procese mensajes de nivel INFO o superior (INFO, WARNING, ERROR, CRITICAL).
    logger.setLevel(logging.INFO)

    return logger
