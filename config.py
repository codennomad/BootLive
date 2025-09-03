import os

# IMPORTANT: Set this to the video ID of your YouTube live stream
VIDEO_ID = ""

# Configuration for scheduled messages
MESSAGE_INTERVAL_MINUTES = 15
SCHEDULED_MESSAGES = [
    "Não se esqueça de se inscrever no canal!",
    "Deixe o seu like para apoiar a live!",
    "Siga-nos nas redes sociais para mais conteúdo!",
]

# Chat commands and their responses
# IMPORTANT: Replace the placeholder links with your actual links!
CHAT_COMMANDS = {
    "!link": "Aqui está o link do canal: https://www.youtube.com/channel/YOUR_CHANNEL_ID",
    "!discord": "Entre no nosso Discord: https://discord.gg/YOUR_INVITE_CODE",
    "!ban": "Usage: !ban <username>",
    "!unban": "Usage: !unban <username>",
    "!load": "Usage: !load <command>",
    "!unload": "Usage: !unload <command>",
    "!reload": "Usage: !reload <command>",
}

# Welcome message for new chat members
# {username} will be replaced with the user's display name
WELCOME_MESSAGE = "Seja bem-vindo(a) ao chat, {username}!"

# Cooldown period in seconds for users to send messages
USER_MESSAGE_COOLDOWN_SECONDS = 5

# Cooldown period in seconds for global commands
GLOBAL_COMMAND_COOLDOWN_SECONDS = 2

# List of moderators (user channel IDs)
MODERATORS = [
    "UC...",  # Replace with the channel ID of a moderator
]

# Command permissions (command: [list of allowed roles])
# Available roles: moderator
COMMAND_PERMISSIONS = {
    "!ban": ["moderator"],
    "!unban": ["moderator"],
    "!load": ["moderator"],
    "!unload": ["moderator"],
    "!reload": ["moderator"],
}
