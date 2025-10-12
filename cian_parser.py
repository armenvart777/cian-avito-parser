"""Парсер объявлений ЦИАН через внутренний JSON API."""

import asyncio
import json
import logging
import random
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from curl_cffi.requests import AsyncSession

from config import (
    DEAL_TYPE,
    LOCATIONS,
    MAX_LISTING_AGE_HOURS,
    MAX_PAGES,
    OBJECT_TYPES,
    OWNER_TYPE,
    REQUEST_DELAY_MAX,
    REQUEST_DELAY_MIN,
    SEEN_IDS_FILE,
    USER_AGENTS,
)

logger = logging.getLogger(__name__)


def _load_seen_ids() -> set[int]:
    """Загрузить ID уже обработанных объявлений."""
    ...


def _save_seen_ids(ids: set[int]) -> None:
    """Сохранить ID обработанных объявлений."""
    ...


def _get_headers() -> dict[str, str]:
    """Сформировать реалистичные HTTP-заголовки."""
    ...


def _build_url(offer_type: str, region_id: int, page: int, district_id: int | None = None) -> str:
    """Построить URL для запроса к ЦИАН."""
    ...


def _extract_json_data(html: str) -> list[dict[str, Any]]:
    """Извлечь данные объявлений из JSON, встроенного в HTML страницы."""
    ...


def _find_offers_in_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Рекурсивно найти массив объявлений в JSON-структуре."""
    ...


def _parse_offer(raw: dict[str, Any], offer_type: str) -> dict[str, Any] | None:
    """Преобразовать сырые данные объявления в нужный формат."""
    ...


def _parse_offers_from_html_fallback(html: str, offer_type: str) -> list[dict[str, Any]]:
    """Fallback: парсинг через BeautifulSoup если JSON не найден."""
    ...


async def parse_new_listings() -> list[dict[str, Any]]:
    """Спарсить новые объявления с ЦИАН.

    Returns:
        Список новых объявлений (которых ещё не было в seen_ids).
    """
    ...
