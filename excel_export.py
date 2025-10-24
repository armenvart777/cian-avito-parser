"""Экспорт объявлений в Excel."""

import logging
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from config import AVITO_EXCEL_FILE, EXCEL_FILE

logger = logging.getLogger(__name__)

COLUMNS = [
    ("Дата", 20),
    ("Источник", 10),
    ("Тип", 12),
    ("Комнаты", 10),
    ("Цена", 18),
    ("Адрес", 45),
    ("Площадь", 12),
    ("Этаж", 10),
    ("Собственник", 18),
    ("Ссылка", 50),
]


def _create_workbook() -> Workbook:
    """Создать новый Excel-файл с заголовками."""
    ...


def save_to_excel(listings: list[dict[str, Any]], source: str = "ЦИАН") -> None:
    """Сохранить объявления в Excel-файл.

    Args:
        listings: Список объявлений.
        source: Источник - "ЦИАН" или "Авито". Определяет файл.
    """
    ...
