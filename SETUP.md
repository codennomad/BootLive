# YouTube Livestream Bot Setup Guide

This guide will help you set up and run the YouTube Livestream Bot on your system.

## Prerequisites

- Python 3.10 or higher
- A Google Account
- Git (optional, for cloning the repository)

## Installation Steps

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd youtube_livestream_bot
```

### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

For development (optional):
```bash
pip install -r requirements-dev.txt
```

### 3. Set up Google Cloud and YouTube Data API

1. **Create a Google Cloud Project**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable the YouTube Data API v3**:
   - In your project's dashboard, go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3" and enable it

3. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" and select "OAuth client ID"
   - Choose "Desktop application" for the application type
   - Click "Create"
   - Download the JSON file and rename it to `client_secret.json`
   - Place it in the root directory of this project

### 4. Configure the Bot

Edit the `config.py` file to customize your bot:

```python
# Set your YouTube live stream video ID
VIDEO_ID = "YOUR_VIDEO_ID_HERE"

# Update command responses
CHAT_COMMANDS = {
    "!link": "Your channel link here",
    "!discord": "Your Discord invite link here",
    # ... other commands
}

# Customize welcome message
WELCOME_MESSAGE = "Welcome to the chat, {username}!"

# Add moderator channel IDs
MODERATORS = [
    "UC...",  # Replace with actual channel IDs
]
```

### 5. Run the Bot

```bash
python main.py
```

On first run, the bot will:
1. Open a browser window for Google OAuth authentication
2. Ask you to grant permissions to access your YouTube account
3. Create a `token.pickle` file to store authentication tokens

## Features

### Available Commands

- `!link` - Shows your channel link
- `!discord` - Shows your Discord invite link
- `!ban <username>` - Bans a user (moderators only)
- `!unban <username>` - Unbans a user (moderators only)
- `!load <command>` - Loads a command module (moderators only)
- `!unload <command>` - Unloads a command module (moderators only)
- `!reload <command>` - Reloads a command module (moderators only)

### Bot Features

- **Real-time Chat Monitoring**: Reads and responds to chat messages
- **Automated Welcome Messages**: Greets new users
- **Scheduled Messages**: Sends periodic reminders
- **User Ban System**: Persistent ban list with file storage
- **Command Cooldowns**: Prevents spam
- **Permission System**: Role-based command access
- **Dynamic Command Loading**: Hot-reload commands without restarting

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing
```

### Code Quality Checks

```bash
# Format code
black .

# Type checking
mypy .
```

### Adding New Commands

1. Create a new file in the `commands/` directory: `commands/mycommand_command.py`
2. Implement the `execute` function:

```python
from types import ModuleType

def execute(config: ModuleType, message: str) -> str:
    """Execute the !mycommand command."""
    # Your command logic here
    return "Command response"
```

3. Add the command to `config.py` if needed:

```python
CHAT_COMMANDS = {
    "!mycommand": "Usage: !mycommand",
    # ... other commands
}

# If the command requires permissions:
COMMAND_PERMISSIONS = {
    "!mycommand": ["moderator"],
    # ... other permissions
}
```

4. The command will be automatically loaded when the bot starts

## Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure `client_secret.json` is in the root directory
   - Delete `token.pickle` and re-authenticate if needed

2. **Video ID Not Found**:
   - Make sure the `VIDEO_ID` in `config.py` is correct
   - Ensure the video is a live stream and is currently active

3. **Permission Denied**:
   - Check that your Google account has access to the YouTube channel
   - Verify the OAuth scopes are correct

4. **Import Errors**:
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

### Getting Help

- Check the logs for detailed error messages
- Ensure your Python version is 3.10 or higher
- Verify all configuration settings in `config.py`

## Security Notes

- Never share your `client_secret.json` or `token.pickle` files
- Add these files to your `.gitignore` if using version control
- Regularly review and update your moderator list
- Monitor bot activity through the console logs
