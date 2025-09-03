import logging
from types import ModuleType
from command_handler import unload_command


def execute(config: ModuleType, message: str) -> str:
    """Execute the unload command."""
    parts = message.split()
    if len(parts) < 2:
        return "Usage: !unload <command>"

    command_to_unload = parts[1].strip()
    if not command_to_unload:
        return "Please provide a valid command name to unload."

    try:
        if unload_command(command_to_unload):
            logging.info(f"Command {command_to_unload} unloaded successfully.")
            return f"Command {command_to_unload} unloaded successfully."
        else:
            logging.warning(f"Failed to unload command {command_to_unload}.")
            return f"Failed to unload command {command_to_unload}. Make sure the command exists."
    except Exception as e:
        logging.error(f"Error unloading command {command_to_unload}: {e}")
        return f"Error unloading command {command_to_unload}: {str(e)}"
