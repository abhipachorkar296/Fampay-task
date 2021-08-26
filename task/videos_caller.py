from apscheduler.events import SchedulerEvent
from apscheduler.schedulers.background import BackgroundScheduler
from task.views import fetch_videos

def begin():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_videos, "interval", seconds=10, id="weather_001",replace_existing=True)
    scheduler.start()
