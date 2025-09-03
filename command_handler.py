# command_handler.py
import os
import importlib
import importlib.util
import sys
import logging
import time
from types import ModuleType
from typing import Dict, Callable, Any, Optional, List

# The type for a command function is a callable that takes the config module and a message, and returns a string.
CommandFunction = Callable[[ModuleType, str], str]
commands: Dict[str, CommandFunction] = {}
last_command_time: float = 0


def has_permission(author_id: str, command: str, config: ModuleType) -> bool:
    """Checks if a user has permission to execute a command."""
    if command not in config.COMMAND_PERMISSIONS:
        return True  # No permission required

    required_roles = config.COMMAND_PERMISSIONS[command]
    user_roles: List[str] = []

    if author_id in config.MODERATORS:
        user_roles.append("moderator")

    for role in required_roles:
        if role in user_roles:
            return True

    return False


def load_command(command_name: str) -> bool:
    """Loads a single command."""
    module_name = f"commands.{command_name}_command"
    logging.info(f"Loading command: {command_name} from {module_name}")
    try:
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
        command_key = f"!{command_name}"
        if hasattr(module, "execute") and callable(module.execute):
            commands[command_key] = module.execute
            logging.info(f"Loaded command: {command_key}")
            return True
    except Exception as e:
        logging.error(f"Failed to load command {command_name}: {e}")
    return False


def unload_command(command_name: str) -> bool:
    """Unloads a single command."""
    command_key = f"!{command_name}"
    if command_key in commands:
        del commands[command_key]
        module_name = f"commands.{command_name}_command"
        if module_name in sys.modules:
            del sys.modules[module_name]
        logging.info(f"Unloaded command: {command_key}")
        return True
    return False


def reload_command(command_name: str) -> bool:
    """Reloads a single command."""
    if unload_command(command_name):
        return load_command(command_name)
    return False


def load_commands() -> None:
    """Dynamically loads all command modules from the commands directory."""
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            command_name = filename.replace("_command.py", "")
            load_command(command_name)


def handle_command(
    command: str, config: ModuleType, author_id: str, message: str
) -> Optional[str]:
    """Executes a command if it exists and the user has permission."""
    global last_command_time
    command_name = message.split(" ")[0]
    logging.info(f"Handling command: {command_name}")
    logging.info(f"Available commands: {commands.keys()}")
    if command_name in commands:
        if has_permission(author_id, command_name, config):
            current_time = time.time()
            if (
                current_time - last_command_time
                < config.GLOBAL_COMMAND_COOLDOWN_SECONDS
            ):
                logging.info(
                    f"Global command cooldown is active. Ignoring command '{message}' from {author_id}."
                )
                return None

            last_command_time = current_time
            response = commands[command_name](config, message)
            return response
        else:
            logging.warning(
                f"User {author_id} does not have permission to execute {command_name}"
            )
            return "You do not have permission to use this command."
    return None
