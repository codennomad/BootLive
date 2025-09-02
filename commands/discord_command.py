# commands/discord_command.py
from types import ModuleType

def execute(config: ModuleType) -> str:
    """Returns the response for the !discord command."""
    return config.CHAT_COMMANDS['!discord']