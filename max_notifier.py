"""Уведомления в MAX мессенджер через Bot API."""

import logging
from typing import Any

import aiohttp

from config import MAX_BOT_TOKEN, MAX_CHAT_ID, MAX_NOTIFY_CHAT_IDS

logger = logging.getLogger(__name__)

MAX_API_URL = "https://platform-api.max.ru/messages"


def _format_message(listing: dict[str, Any]) -> str:
    """Сформировать текст уведомления."""
    ...


async def _send_to_chat(session: aiohttp.ClientSession, chat_id: str,
                        message_text: str, headers: dict, listing_id: str) -> bool:
    """Отправить сообщение в один чат."""
    ...


async def send_notification(listing: dict[str, Any]) -> bool:
    """Отправить уведомление о новом объявлении всем получателям в MAX.

    Returns:
        True если отправлено хотя бы одному получателю, False при ошибке.
    """
    ...
