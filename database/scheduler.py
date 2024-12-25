from apscheduler.schedulers.background import BackgroundScheduler
from .db_utils import update_debts
from logger import app_logger


def start_task(connection):
    """Функция для старта фоновой задачи по обновлению долгов"""

    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: update_debts(connection), 'cron', day=15, hour=0)
    scheduler.start()
    app_logger.info("Планировщик задач запущен")

    return scheduler


def end_task(scheduler):
    """Функция для завершения работы планировщика"""

    scheduler.shutdown()
    app_logger.info("Планировщик задач остановлен")

    return None


