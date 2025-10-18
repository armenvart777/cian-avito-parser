"""Парсер объявлений Авито через cookie-based подход.

Стратегия:
1. curl_cffi + impersonate + ASOCKS прокси -> запрашиваем поисковые страницы
2. Извлечение данных из встроенного JSON в HTML (data-mfe-state)
3. При блокировке - ротация прокси + длинная пауза
4. Увеличенные задержки для стабильности
"""

import asyncio
import json
import logging
import random
import re
import time
import html as html_mod
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from curl_cffi.requests import AsyncSession

from config import (
    AVITO_CATEGORIES,
    AVITO_LOCATIONS,
    AVITO_MAX_PAGES,
    AVITO_SEEN_IDS_FILE,
    MAX_LISTING_AGE_HOURS,
    PROXY_POOL_ASOCKS,
    USER_AGENTS,
)

logger = logging.getLogger(__name__)

AVITO_BASE = "https://www.avito.ru"

_IMPERSONATE_LIST = [
    "chrome120", "chrome123", "chrome124", "chrome131", "chrome136",
]

_DELAY_MIN = 20.0
_DELAY_MAX = 40.0
_DELAY_BETWEEN_CATEGORIES = (30.0, 60.0)
_DELAY_BETWEEN_LOCATIONS = (60.0, 120.0)

_cookie_cache: dict[str, Any] = {
    "cookies": {},
    "user_agent": "",
    "timestamp": 0,
    "proxy_idx": 0,
    "consecutive_blocks": 0,
}

_COOKIE_TTL = 20 * 60
_MAX_CONSECUTIVE_BLOCKS = 2

_seen_ids_corrupted = False


def _load_seen_ids() -> set[str]:
    ...


def _save_seen_ids(ids: set[str]) -> None:
    ...


def _get_proxy(idx: int | None = None) -> tuple[str, int]:
    ...


def _get_headers(user_agent: str, referer: str | None = None) -> dict[str, str]:
    ...


def _build_url(location_path: str, category_path: str, page: int) -> str:
    ...


def _is_blocked(html: str) -> bool:
    ...


async def _acquire_cookies(proxy_url: str) -> tuple[dict[str, str], str]:
    """Получить cookies через GET на Авито."""
    ...


async def _ensure_cookies() -> tuple[dict[str, str], str]:
    ...


async def _fetch_page_curl(
    url: str,
    cookies: dict[str, str],
    user_agent: str,
    referer: str | None = None,
) -> tuple[str | None, bool]:
    ...


async def _fetch_avito_page(url: str, referer: str | None = None) -> tuple[str | None, bool]:
    """Загрузить страницу с ротацией прокси при блокировке."""
    ...


def _extract_json_data(page_html: str) -> list[dict[str, Any]]:
    """Извлечь объявления из JSON, встроенного в HTML Авито."""
    ...


def _find_items_in_data(data: Any) -> list[dict[str, Any]]:
    ...


def _parse_item_from_json(raw: dict[str, Any], object_type: str) -> dict[str, Any] | None:
    ...


def _matches_address_filter(item: dict[str, Any], address_filter: list[str] | None) -> bool:
    ...


async def parse_new_avito_listings() -> list[dict[str, Any]]:
    """Спарсить новые объявления с Авито.

    Стратегия: только 1 страница на категорию (свежие),
    увеличенные паузы, быстрая ротация прокси.
    """
    ...
