import os

# IMPORTANT: Set this to the video ID of your YouTube live stream
VIDEO_ID = ""

# Configuration for scheduled messages
MESSAGE_INTERVAL_MINUTES = 15
SCHEDULED_MESSAGES = [
    "Não se esqueça de se inscrever no canal!",
    "Deixe o seu like para apoiar a live!",
    "Siga-nos nas redes sociais para mais conteúdo!"
]

# Chat commands and their responses
# IMPORTANT: Replace the placeholder links with your actual links!
CHAT_COMMANDS = {
    "!link": "Aqui está o link do canal: https://www.youtube.com/channel/YOUR_CHANNEL_ID",
    "!discord": "Entre no nosso Discord: https://discord.gg/YOUR_INVITE_CODE"
}

# Welcome message for new chat members
# {username} will be replaced with the user's display name
WELCOME_MESSAGE = "Seja bem-vindo(a) ao chat, {username}!"
