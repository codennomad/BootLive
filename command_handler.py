# command_handler.py
import os
import importlib
import logging
from types import ModuleType
from typing import Dict, Callable, Any, Optional

# The type for a command function is a callable that takes the config module and returns a string.
CommandFunction = Callable[[ModuleType], str]
commands: Dict[str, CommandFunction] = {}

def load_commands() -> None:
    """Dynamically loads all command modules from the commands directory."""
    commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = f"commands.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                command_name = f"!{filename.replace('_command.py', '')}"
                if hasattr(module, 'execute') and callable(module.execute):
                    commands[command_name] = module.execute
                    logging.info(f"Loaded command: {command_name}")
            except Exception as e:
                logging.error(f"Failed to load command from {filename}: {e}")

def handle_command(command: str, config: ModuleType) -> Optional[str]:
    """Executes a command if it exists."""
    if command in commands:
        return commands[command](config)
    return None
