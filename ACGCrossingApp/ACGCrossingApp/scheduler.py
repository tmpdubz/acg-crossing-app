import time
'''
some good an easy docmentation to use 
https://github.com/jarekwg/django-apscheduler
https://medium.com/@kevin.michael.horan/scheduling-tasks-in-django-with-the-advanced-python-scheduler-663f17e868e6
https://apscheduler.readthedocs.io/en/latest/userguide.html#starting-the-scheduler
'''
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
