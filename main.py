import time
import threading
import random
import logging
from typing import Set, Optional

import config
from logger_setup import setup_logger
from command_handler import load_commands, handle_command
from youtube_api import (
    get_youtube_service, 
    get_live_chat_id, 
    get_chat_messages, 
    send_chat_message, 
    get_own_channel_name
)
from googleapiclient.discovery import Resource

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
            time.sleep(60) # Wait a minute before retrying


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
        logging.warning("Could not determine bot's channel name. The bot might respond to its own messages.")

    if not config.VIDEO_ID:
        logging.critical("VIDEO_ID is not set in config.py. Please set it to your YouTube Live Stream Video ID.")
        return

    live_chat_id = get_live_chat_id(youtube, config.VIDEO_ID)

    if not live_chat_id:
        return

    logging.info(f"Successfully connected to live chat. Chat ID: {live_chat_id}")

    scheduler_thread = threading.Thread(target=message_scheduler, args=(youtube, live_chat_id))
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logging.info(f"Message scheduler started. Will send a message every {config.MESSAGE_INTERVAL_MINUTES} minutes.")

    logging.info("Starting to fetch chat messages, listen for commands, and welcome new users...")
    next_page_token: Optional[str] = None
    seen_users: Set[str] = set()

    try:
        while True:
            chat_response = get_chat_messages(youtube, live_chat_id, next_page_token)
            if not chat_response:
                logging.warning("Could not retrieve chat messages. The stream might have ended.")
                break

            for item in chat_response['items']:
                author_details = item['authorDetails']
                author_id = author_details['channelId']
                author_name = author_details['displayName']
                message = item['snippet']['displayMessage'].strip()
                
                logging.info(f"Chat: {author_name}: {message}")

                # Welcome new users
                if author_id not in seen_users:
                    seen_users.add(author_id)
                    if not (bot_channel_name and author_name == bot_channel_name):
                        welcome_message = config.WELCOME_MESSAGE.format(username=author_name)
                        logging.info(f"Welcoming new user: {author_name}")
                        send_chat_message(youtube, live_chat_id, welcome_message)

                if bot_channel_name and author_name == bot_channel_name:
                    continue

                response = handle_command(message, config)
                if response:
                    logging.info(f"Responding to command '{message}' with: {response}")
                    send_chat_message(youtube, live_chat_id, response)

            next_page_token = chat_response.get('nextPageToken')
            polling_interval = chat_response.get('pollingIntervalMillis', 10000) / 1000

            time.sleep(polling_interval)

    except KeyboardInterrupt:
        logging.info("\nStopping bot...")
    finally:
        stop_scheduler.set()
        scheduler_thread.join()
        logging.info("Bot stopped.")

if __name__ == "__main__":
    main()
