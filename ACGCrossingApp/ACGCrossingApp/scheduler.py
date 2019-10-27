import time

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=300, replace_existing=True)
def test_job():
    print("I'm a test job!")
register_events(scheduler)

scheduler.start()
print("Scheduler started!")
