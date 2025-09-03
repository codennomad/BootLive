[![Build Status](https://img.shields.io/github/actions/workflow/status/<user>/<repo>/ci.yml)](https://github.com/<user>/<repo>/actions)
[![License](https://img.shields.io/badge/license-MIT-informational)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![type checking: mypy](https://img.shields.io/badge/type--checking-mypy-informational)](http://mypy-lang.org/)
[![coverage](https://img.shields.io/badge/coverage-xx%25-lightgrey)](https://github.com/<user>/<repo>)
[![last commit](https://img.shields.io/github/last-commit/<user>/<repo>)](https://github.com/<user>/<repo>/commits/main)
[![issues](https://img.shields.io/github/issues/<user>/<repo>)](https://github.com/<user>/<repo>/issues)

# YouTube Live Stream Bot

A versatile and modular bot for interacting with YouTube live stream chats. Built with Python, it provides a solid foundation for creating custom chat bots with features like automated messaging, command handling, and real-time user interaction.

## Table of Contents

- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)

## Features

### Core Bot Features
- **Live Chat Connection**: Connects to any public YouTube live stream chat.
- **Real-time Message Reading**: Reads chat messages in real time.
- **Smart Message Processing**: Only processes new messages after startup, avoiding reprocessing of chat history.
- **Scheduled Messages**: Periodically sends automated messages to the chat (e.g., subscription reminders).
- **New User Welcome**: Automatically detects when a new user chats for the first time and sends them a customizable welcome message.
- **User Ban System**: Persistent ban list with JSON file storage - banned users' messages are automatically ignored.
- **Command Cooldowns**: Global and per-user cooldown system to prevent spam.
- **Permission System**: Role-based command access with moderator privileges.

### Advanced Command System
- **Modular Architecture**: Easy-to-extend command system with automatic loading.
- **Dynamic Command Management**: Load, unload, and reload commands without restarting the bot.
- **Hot-Reload Capability**: Modify command code and reload it instantly during runtime.
- **Built-in Commands**:
  - `!link` - Shows your channel link
  - `!discord` - Shows your Discord invite link
  - `!ban <username>` - Bans a user from interacting (moderators only)
  - `!unban <username>` - Unbans a previously banned user (moderators only)
  - `!load <command>` - Loads a command module (moderators only)
  - `!unload <command>` - Unloads a command module (moderators only)
  - `!reload <command>` - Reloads a command module (moderators only)

### Development & Quality Assurance
- **Comprehensive Testing**: Full test suite with 21 tests covering all functionality.
- **Type Safety**: Complete type annotations with mypy compliance.
- **Code Quality**: Black formatting and strict linting standards.
- **Error Handling**: Robust error handling and recovery mechanisms.
- **Detailed Logging**: Comprehensive logging for monitoring and debugging.
- **CI/CD Pipeline**: Pre-configured GitHub Actions workflow for continuous integration.
- **Test Coverage**: Detailed coverage reporting to ensure code quality.

## Setup and Installation

### Prerequisites

- Python 3.10 or higher.
- A Google Account.

### 1. Set up Google Cloud and YouTube Data API

Before running the bot, you need to authorize it to use the YouTube Data API on your behalf.

1.  **Create a Google Cloud Project**: Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a new project.
2.  **Enable the YouTube Data API v3**: In your project's dashboard, go to "APIs & Services" > "Library", search for "YouTube Data API v3", and enable it.
3.  **Create OAuth 2.0 Credentials**:
    -   Go to "APIs & Services" > "Credentials".
    -   Click "Create Credentials" and select "OAuth client ID".
    -   Choose "Desktop application" for the application type.
    -   Click "Create". A pop-up will show your Client ID and Client secret.
    -   Click the **DOWNLOAD JSON** button.
    -   Rename the downloaded file to `client_secret.json` and place it in the root directory of this project.

### 2. Install Dependencies

1.  Clone this repository to your local machine.
2.  Navigate to the project directory.
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the bot, you must edit the `config.py` file to set your specific parameters:

1.  **`VIDEO_ID`**: Set this to the ID of the YouTube live stream you want to connect to.
    ```python
    VIDEO_ID = "YOUR_VIDEO_ID_HERE"
    ```
2.  **`CHAT_COMMANDS`**: Update the responses for the commands. You can also add new commands here.
    ```python
    CHAT_COMMANDS = {
        "!link": "Aqui está o link do canal: https://www.youtube.com/your-channel",
        "!discord": "Entre no nosso Discord: https://discord.gg/your-invite"
    }
    ```
3.  **`WELCOME_MESSAGE`**: Customize the message sent to new chat participants.
    ```python
    WELCOME_MESSAGE = "Seja bem-vindo(a) ao chat, {username}!"
    ```

## Usage

To run the bot, execute the `main.py` script from the root of the project directory:

```bash
python main.py
```

### First-time Authentication

The first time you run the bot, it will open a new tab in your web browser and ask you to authorize it to access your YouTube account. After you grant permission, it will create a `token.pickle` file in the project directory. This file stores your authentication token so you won't have to log in every time.

**Important**: Do not share the `client_secret.json` or `token.pickle` files.

## Running Tests

The project includes a full test suite to ensure reliability.

1.  Install the development dependencies:
    ```bash
    pip install -r requirements-dev.txt
    ```
2.  Run the tests from the project's root directory:
    ```bash
    python -m unittest discover -s youtube_livestream_bot/tests -t youtube_livestream_bot
    ```

## CI/CD Pipeline

This project is equipped with a Continuous Integration (CI) pipeline using GitHub Actions, located at `.github/workflows/ci.yml`.

This workflow automatically triggers on every `push` and `pull_request` to the `main` branch. It performs the following checks:

-   Installs all dependencies.
-   Checks code formatting with `black`.
-   Performs static type checking with `mypy`.
-   Runs the complete test suite with `pytest` and calculates code coverage.

This ensures that all code committed to the repository is well-formatted, type-safe, and passes all tests.
