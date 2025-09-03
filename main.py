import time
import threading
import random
import logging
from typing import Set, Optional, Dict

import config
from logger_setup import setup_logger
from command_handler import load_commands, handle_command
from youtube_api import (
    get_youtube_service,
    get_live_chat_id,
    get_chat_messages,
    send_chat_message,
    get_own_channel_name,
)
from googleapiclient.discovery import Resource
from commands.ban_command import load_banned_users

# A flag to signal the message scheduler thread to stop
stop_scheduler = threading.Event()


def message_scheduler(youtube: Resource, live_chat_id: str) -> None:
    """Sends a random scheduled message every X minutes."""
    while not stop_scheduler.is_set():
        try:
            # Wait for the specified interval, but check for the stop signal every second
            for _ in range(config.MESSAGE_INTERVAL_MINUTES * 60):
                if stop_scheduler.is_set():
                    return
                time.sleep(1)

            message = random.choice(config.SCHEDULED_MESSAGES)
            logging.info(f"Sending scheduled message: {message}")
            send_chat_message(youtube, live_chat_id, message)

        except Exception as e:
            logging.error(f"An error occurred in the message scheduler: {e}")
            # Continue running even if one attempt fails
            time.sleep(60)  # Wait a minute before retrying


def main() -> None:
    """Main function for the YouTube bot."""
    setup_logger()
    load_commands()

    youtube = get_youtube_service()
    if not youtube:
        logging.critical("Failed to initialize YouTube service. Exiting.")
        return

    bot_channel_name = get_own_channel_name(youtube)
    if bot_channel_name:
        logging.info(f"Bot is running as channel: {bot_channel_name}")
    else:
        logging.warning(
            "Could not determine bot's channel name. The bot might respond to its own messages."
        )

    if not config.VIDEO_ID:
        logging.critical(
            "VIDEO_ID is not set in config.py. Please set it to your YouTube Live Stream Video ID."
        )
        return

    live_chat_id = get_live_chat_id(youtube, config.VIDEO_ID)

    if not live_chat_id:
        return

    logging.info(f"Successfully connected to live chat. Chat ID: {live_chat_id}")

    scheduler_thread = threading.Thread(
        target=message_scheduler, args=(youtube, live_chat_id)
    )
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logging.info(
        f"Message scheduler started. Will send a message every {config.MESSAGE_INTERVAL_MINUTES} minutes."
    )

    logging.info(
        "Starting to fetch chat messages, listen for commands, and welcome new users..."
    )
    next_page_token: Optional[str] = None
    seen_users: Set[str] = set()
    user_last_message_time: Dict[str, float] = {}

    # Record startup time to avoid processing old messages
    startup_time = time.time()
    is_first_fetch = True

    logging.info("Skipping existing chat history to avoid reprocessing old messages...")

    try:
        while True:
            chat_response = get_chat_messages(youtube, live_chat_id, next_page_token)
            if not chat_response:
                logging.warning(
                    "Could not retrieve chat messages. The stream might have ended."
                )
                break

            for item in chat_response["items"]:
                author_details = item["authorDetails"]
                author_id = author_details["channelId"]
                author_name = author_details["displayName"]
                message = item["snippet"]["displayMessage"].strip()

                # Get message timestamp
                message_time_str = item["snippet"]["publishedAt"]
                # Convert ISO 8601 timestamp to Unix timestamp
                from datetime import datetime

                message_time = datetime.fromisoformat(
                    message_time_str.replace("Z", "+00:00")
                ).timestamp()

                # Skip old messages on first fetch to avoid reprocessing chat history
                if is_first_fetch and message_time < startup_time:
                    logging.debug(f"Skipping old message from {author_name}: {message}")
                    continue

                logging.info(f"Chat from {author_name}: {message}")

                # Ignore messages from the bot itself
                if bot_channel_name and author_name == bot_channel_name:
                    continue

                # Check if user is banned
                banned_users = load_banned_users()
                if author_name in banned_users:
                    logging.info(f"Ignoring message from banned user: {author_name}")
                    continue

                # Rate limiting
                current_time = time.time()
                if author_id in user_last_message_time:
                    last_message_time = user_last_message_time[author_id]
                    if (
                        current_time - last_message_time
                        < config.USER_MESSAGE_COOLDOWN_SECONDS
                    ):
                        logging.info(
                            f"User {author_name} is on cooldown. Ignoring message."
                        )
                        continue

                user_last_message_time[author_id] = current_time

                # Welcome new users (but only for new messages, not old ones)
                if author_id not in seen_users:
                    seen_users.add(author_id)
                    welcome_message = config.WELCOME_MESSAGE.format(
                        username=author_name
                    )
                    logging.info(f"Welcoming new user: {author_name}")
                    send_chat_message(youtube, live_chat_id, welcome_message)
                    # This welcome message should also be subject to cooldown, so we continue
                    continue

                response = handle_command(message, config, author_id, message)
                if response:
                    logging.info(
                        f"Responding to command '{message}' from {author_name} with: {response}"
                    )
                    send_chat_message(youtube, live_chat_id, response)

            # After first fetch, we can process all subsequent messages
            if is_first_fetch:
                is_first_fetch = False
                logging.info(
                    "Finished skipping old messages. Now processing new messages in real-time."
                )

            next_page_token = chat_response.get("nextPageToken")
            polling_interval = chat_response.get("pollingIntervalMillis", 10000) / 1000

            time.sleep(polling_interval)

    except KeyboardInterrupt:
        logging.info("\nStopping bot...")
    finally:
        stop_scheduler.set()
        scheduler_thread.join()
        logging.info("Bot stopped.")


if __name__ == "__main__":
    main()
