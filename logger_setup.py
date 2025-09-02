# logger_setup.py
import logging

def setup_logger() -> None:
    """Sets up the root logger for the application."""
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set the lowest level of messages to handle

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    # Check if handlers are already present to avoid duplication
    if not logger.handlers:
        logger.addHandler(console_handler)
