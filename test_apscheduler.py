# import datetime
# import os
# import time
#
# from apscheduler.executors.pool import ProcessPoolExecutor
# from apscheduler.schedulers.background import BackgroundScheduler
# from pytz import utc
#
# executors = {
#     "default": ProcessPoolExecutor(10),
#     "poolexecutor": ProcessPoolExecutor(10)
# }
#
# sched = BackgroundScheduler(executors=executors, timezone=utc)
#
#
# def hello(tsk_id):
#     print("%s hello with pid:%r" % (tsk_id, os.getpid()))
#     next_run_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
#     sched.add_job(hello, "interval", seconds=3, args=[tsk_id])
#     print("add job ok and exit")
#
#
# def main():
#     for i in range(10):
#         sched.add_job(func=hello, executor="poolexecutor", args=[i],
#                       next_run_time=datetime.datetime.utcnow() + datetime.timedelta(
#                           seconds=3))
#     sched.start()
#     while True:
#         time.sleep(1)
#
#
# if __name__ == '__main__':
#     main()
import datetime as dt
import os
import time
from datetime import datetime

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(
    executors={
        "processpool": ThreadPoolExecutor(10)
    })


def tick():
    next_run_at = datetime.now() + dt.timedelta(seconds=3.0)
    print(
        'Tick! The time is: %s, run next at:%s' % (datetime.now(), next_run_at))
    scheduler.add_job(tick, next_run_time=next_run_at, executor="processpool", id="hello kitty")
    print("pid:%r" % os.getpid())


if __name__ == '__main__':
    next_run_at = datetime.now() + dt.timedelta(seconds=3.0)
    scheduler.add_job(tick, next_run_time=next_run_at, executor="processpool", id="hello kitty")
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    while True:
        time.sleep(1)
        pass
