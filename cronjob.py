from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

class MyScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def add_job(self, task, minutes=60, job_id="", kwargs=None):
        self.scheduler.add_job(
            func=task,
            trigger=IntervalTrigger(minutes=1),
            minutes=minutes,
            id=job_id,
            kwargs=kwargs or {}
        )
        print("job added success")
    def start_job(self): 
        if not self.scheduler.running:
            self.scheduler.start()

    def pause_job(self, job_id):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        self.scheduler.resume_job(job_id)

    def stop_scheduler(self):
        self.scheduler.shutdown()
