"""Конфигурация парсера ЦИАН + Авито."""

import os
from dotenv import load_dotenv

load_dotenv()

# ===== MAX Мессенджер =====
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN", "")
MAX_CHAT_ID = os.getenv("MAX_CHAT_ID", "")
MAX_NOTIFY_CHAT_IDS = [x.strip() for x in os.getenv("MAX_NOTIFY_CHAT_IDS", "").split(",") if x.strip()]

# ===== Интервал проверки =====
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "1800"))  # 30 минут (в секундах)

# ===== Файлы =====
EXCEL_FILE = "cian_voronezh.xlsx"
AVITO_EXCEL_FILE = "avito_voronezh.xlsx"
SEEN_IDS_FILE = "seen_ids.json"
AVITO_SEEN_IDS_FILE = "avito_seen_ids.json"
LOG_FILE = "parser.log"

# ===== Параметры парсинга =====
DEAL_TYPE = "sale"
OBJECT_TYPES = ["flat", "house"]  # квартиры + дома
OWNER_TYPE = 1  # 1 = только частные лица (is_by_homeowner)

# ===== Локации =====
LOCATIONS = [
    {
        "name": "Воронеж, Коминтерновский район",
        "region": 4713,
        "district": 866,
    },
    {
        "name": "Воронежская обл., Рамонский район",
        "region": 6360,
        "district": None,
    },
]

# ===== HTTP =====
REQUEST_DELAY_MIN = 8.0
REQUEST_DELAY_MAX = 15.0
MAX_PAGES = int(os.getenv("MAX_PAGES", "3"))
MAX_LISTING_AGE_HOURS = int(os.getenv("MAX_LISTING_AGE_HOURS", "12"))

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

# ===== Прокси =====
PROXY_URL = os.getenv("PROXY_URL", "http://proxy.froxy.com:9000")
FROXY_AUTH = os.getenv("FROXY_AUTH", "")
PROXY_POOL_ASOCKS = [x.strip() for x in os.getenv("PROXY_POOL_ASOCKS", "").split(",") if x.strip()]

# ===== Авито =====
AVITO_LOCATIONS = [
    {
        "name": "Воронеж, Коминтерновский район",
        "url_path": "voronezh",
        "address_filter": [
            "коминтерновск",
            "Московский проспект", "проспект Труда", "Рабочий проспект",
            "бульвар Победы", "Олимпийский бульвар",
            "Хользунова", "Шишкова", "Владимира Невского",
            "60 Армии", "Маршала Жукова",
            "Генерала Лизюкова", "Антонова-Овсеенко",
        ],
    },
    {
        "name": "Воронежская обл., Рамонский район",
        "url_path": "ramon",
        "address_filter": None,
    },
]

AVITO_CATEGORIES = [
    {
        "name": "Квартиры",
        "category_path": "kvartiry/prodam-ASgBAgICAUSSA8YQ",
        "object_type": "квартира",
    },
    {
        "name": "Дома",
        "category_path": "doma_dachi_kottedzhi/prodam-ASgBAgICAUSUA8gQ",
        "object_type": "дом",
    },
]

AVITO_OWNER_FILTER = "user=1"
AVITO_MAX_PAGES = int(os.getenv("AVITO_MAX_PAGES", "3"))
