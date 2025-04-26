from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import threading

class RewardScheduler:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        with RewardScheduler._lock:
            if not self.scheduler.running:
                self.scheduler.add_job(self.calculate_daily_rewards, 'interval', hours=24)
                self.scheduler.start()
                print("Scheduler started.")
            else:
                print("Scheduler already running.")

    def calculate_daily_rewards(self):
        print("Calculating ... ", datetime.now())

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance
