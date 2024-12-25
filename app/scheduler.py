from apscheduler.schedulers.background import BackgroundScheduler
from database import connection, update_debts


scheduler = BackgroundScheduler()
scheduler.add_job(lambda: update_debts(connection), 'cron', day=15, hour=0)
scheduler.start()
