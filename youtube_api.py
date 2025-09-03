import os
import pickle
import logging
from typing import Optional, Any, Dict, List

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

# The SCOPES contain the permissions the bot will request from the user.
SCOPES: List[str] = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_youtube_service() -> Optional[Resource]:
    """
    Builds and returns an authenticated YouTube service object.
    Handles OAuth 2.0 flow.
    """
    credentials = None
    token_path = "token.pickle"
    client_secrets_path = "client_secret.json"

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not os.path.exists(client_secrets_path):
                logging.error(
                    "client_secret.json not found. Please download it from the Google Cloud Console."
                )
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_path, SCOPES
            )
            credentials = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)


def get_live_chat_id(youtube: Resource, video_id: str) -> Optional[str]:
    """Gets the live chat ID for a given video ID."""
    try:
        request = youtube.videos().list(part="liveStreamingDetails", id=video_id)
        response: Dict[str, Any] = request.execute()

        if not response.get("items"):
            logging.error(f"Video with ID '{video_id}' not found.")
            return None

        live_streaming_details: Optional[Dict[str, Any]] = response["items"][0].get(
            "liveStreamingDetails"
        )
        if not live_streaming_details:
            logging.error(
                f"Video with ID '{video_id}' is not a live stream or has no live chat."
            )
            return None

        live_chat_id: Optional[str] = live_streaming_details.get("activeLiveChatId")
        if not live_chat_id:
            logging.error(f"Could not find live chat ID for video ID '{video_id}'.")
            return None

        return live_chat_id
    except HttpError as e:
        logging.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None


def get_chat_messages(
    youtube: Resource, live_chat_id: str, page_token: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Gets live chat messages."""
    try:
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id, part="snippet,authorDetails", pageToken=page_token
        )
        response: Dict[str, Any] = request.execute()
        return response
    except HttpError as e:
        logging.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None


def send_chat_message(
    youtube: Resource, live_chat_id: str, message_text: str
) -> Optional[Dict[str, Any]]:
    """Sends a message to the live chat."""
    try:
        request = youtube.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {"messageText": message_text},
                }
            },
        )
        response: Dict[str, Any] = request.execute()
        return response
    except HttpError as e:
        logging.error(
            f"An HTTP error {e.resp.status} occurred while sending message: {e.content}"
        )
        return None


def get_own_channel_name(youtube: Resource) -> Optional[str]:
    """Gets the channel name of the authenticated user."""
    try:
        request = youtube.channels().list(part="snippet", mine=True)
        response: Dict[str, Any] = request.execute()
        if not response.get("items"):
            logging.warning(
                "Could not retrieve authenticated user's channel information."
            )
            return None
        return response["items"][0]["snippet"]["title"]
    except HttpError as e:
        logging.error(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None
