from apscheduler.schedulers.background import BackgroundScheduler
from .db_utils import reset_to_zero_debt, reset_to_zero_readings
from logger import app_logger


def schedule_reset_debt(connection):
    reset_to_zero_debt(connection)


def schedule_reset_readings(connection):
    reset_to_zero_readings(connection)


def run_background_tasks(connection):
    """
    Функция для старта фоновых задач по обновлению долгов и сбросу показаний счётчиков.

    Параметры:
    1. connection - подключение к базе данных
"""

    scheduler = BackgroundScheduler()

    try:
        scheduler.add_job(schedule_reset_debt, 'cron', day=15, hour=0, args=[connection])
        app_logger.info("Задача reset_to_zero_debt успешно добавлена.")
    except Exception as e:
        app_logger.error(f"Ошибка при добавлении задачи reset_to_zero_debt: {e}")

    try:
        scheduler.add_job(schedule_reset_readings, 'cron', day=15, hour=0, args=[connection])
        app_logger.info("Задача reset_to_zero_readings успешно добавлена.")
    except Exception as e:
        app_logger.error(f"Ошибка при добавлении задачи reset_to_zero_readings: {e}")

    scheduler.start()
    app_logger.info("Планировщик задач запущен")

    return scheduler


def end_task(scheduler):
    """Функция для завершения работы планировщика"""

    scheduler.shutdown()
    app_logger.info("Планировщик задач остановлен")

    return None
