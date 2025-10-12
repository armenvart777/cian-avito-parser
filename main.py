"""Точка входа парсера ЦИАН + Авито.

Основной цикл: парсинг ЦИАН → парсинг Авито → Excel → уведомления MAX → пауза.
"""

import asyncio
import logging
import os
import signal
import sys

from config import CHECK_INTERVAL, LOG_FILE

PID_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parser.pid")


def _check_single_instance():
    """Убедиться что запущен только один экземпляр."""
    if os.path.exists(PID_FILE):
        with open(PID_FILE) as f:
            old_pid = int(f.read().strip())
        try:
            os.kill(old_pid, 0)  # проверяем жив ли процесс
            print(f"Парсер уже запущен (PID {old_pid}). Выход.")
            sys.exit(1)
        except OSError:
            pass  # процесс мёртв, можно запускать
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))
from cian_parser import parse_new_listings as parse_cian
from avito_parser import parse_new_avito_listings as parse_avito
from excel_export import save_to_excel
from max_notifier import send_notification

_shutdown = False


def _setup_logging() -> None:
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # уже настроен
    root_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, date_format))
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format, date_format))
    root_logger.addHandler(file_handler)


def _handle_shutdown(signum: int, frame: object) -> None:
    global _shutdown
    _shutdown = True
    logging.getLogger(__name__).info("Получен сигнал завершения, останавливаюсь...")


async def _process_listings(listings: list[dict], source: str, logger) -> None:
    """Сохранить в Excel и отправить уведомления."""
    if not listings:
        return

    logger.info("[%s] Найдено %d новых объявлений", source, len(listings))

    # Добавляем source в каждое объявление
    for item in listings:
        item.setdefault("source", source)

    # Excel
    save_to_excel(listings, source)

    # Уведомления (макс. 10 за раз)
    MAX_NOTIFY = 10
    to_notify = listings[:MAX_NOTIFY]
    if len(listings) > MAX_NOTIFY:
        logger.info("[%s] Отправляю %d из %d уведомлений", source, MAX_NOTIFY, len(listings))

    sent_count = 0
    for listing in to_notify:
        success = await send_notification(listing)
        if success:
            sent_count += 1
        await asyncio.sleep(1)

    logger.info("[%s] Отправлено %d/%d уведомлений", source, sent_count, len(listings))


async def main() -> None:
    _setup_logging()
    logger = logging.getLogger(__name__)

    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    interval_min = CHECK_INTERVAL // 60
    logger.info(
        "Парсер ЦИАН + Авито запущен. Проверка каждые %d минут.",
        interval_min,
    )

    while not _shutdown:
        try:
            logger.info("--- Начинаю проверку ---")
            cian_listings = []
            avito_listings = []

            # 1. ЦИАН
            try:
                cian_listings = await parse_cian()
                await _process_listings(cian_listings, "ЦИАН", logger)
            except Exception as e:
                logger.error("Ошибка парсинга ЦИАН: %s", e, exc_info=True)

            # Пауза между парсерами
            if not _shutdown:
                await asyncio.sleep(5)

            # 2. Авито
            try:
                avito_listings = await parse_avito()
                await _process_listings(avito_listings, "Авито", logger)
            except Exception as e:
                logger.error("Ошибка парсинга Авито: %s", e, exc_info=True)

            if not cian_listings and not avito_listings:
                logger.info("Новых объявлений нет")

        except Exception as e:
            logger.error("Ошибка в основном цикле: %s", e, exc_info=True)

        # Ожидание
        for _ in range(CHECK_INTERVAL):
            if _shutdown:
                break
            await asyncio.sleep(1)

    logger.info("Парсер остановлен.")


if __name__ == "__main__":
    _check_single_instance()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПарсер остановлен по Ctrl+C")
    finally:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
