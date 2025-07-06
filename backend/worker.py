from library.scheduler import StatsScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sscheduler = StatsScheduler()
scheduler = BackgroundScheduler()

scheduler.add_job(
    func=sscheduler.log_daily_stats,
    trigger=IntervalTrigger(minutes=30),
    id='stats_logging_job',
    name='Log daily stats every 30 minutes',
    replace_existing=True
)

scheduler.start()
logger.info("Stats scheduler started. Will log stats every 30 minutes.")

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    try:
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        pass