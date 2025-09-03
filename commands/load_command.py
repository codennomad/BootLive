import logging
from types import ModuleType
from command_handler import load_command


def execute(config: ModuleType, message: str) -> str:
    """Execute the load command."""
    parts = message.split()
    if len(parts) < 2:
        return "Usage: !load <command>"

    command_to_load = parts[1].strip()
    if not command_to_load:
        return "Please provide a valid command name to load."

    try:
        if load_command(command_to_load):
            logging.info(f"Command {command_to_load} loaded successfully.")
            return f"Command {command_to_load} loaded successfully."
        else:
            logging.warning(f"Failed to load command {command_to_load}.")
            return f"Failed to load command {command_to_load}. Make sure the command file exists."
    except Exception as e:
        logging.error(f"Error loading command {command_to_load}: {e}")
        return f"Error loading command {command_to_load}: {str(e)}"
