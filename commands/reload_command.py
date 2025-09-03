import logging
from types import ModuleType
from command_handler import reload_command


def execute(config: ModuleType, message: str) -> str:
    """Execute the reload command."""
    parts = message.split()
    if len(parts) < 2:
        return "Usage: !reload <command>"

    command_to_reload = parts[1].strip()
    if not command_to_reload:
        return "Please provide a valid command name to reload."

    try:
        if reload_command(command_to_reload):
            logging.info(f"Command {command_to_reload} reloaded successfully.")
            return f"Command {command_to_reload} reloaded successfully."
        else:
            logging.warning(f"Failed to reload command {command_to_reload}.")
            return f"Failed to reload command {command_to_reload}. Make sure the command exists."
    except Exception as e:
        logging.error(f"Error reloading command {command_to_reload}: {e}")
        return f"Error reloading command {command_to_reload}: {str(e)}"
