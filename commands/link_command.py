# commands/link_command.py
from types import ModuleType

def execute(config: ModuleType) -> str:
    """Returns the response for the !link command."""
    return config.CHAT_COMMANDS['!link']