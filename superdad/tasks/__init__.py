import datetime
from typing import List, Any

from .depthy import Depthy
from .kliner import KLiner
from .pricy import Pricy
from .trendy import Trendy


class TaskControl:
    STOP = -1


def next_tick(sec):
    if sec == 0:
        return 0
    return datetime.datetime.now() + datetime.timedelta(seconds=sec)


def add_task(f, app, wait_before: int = 0, task_id: str = "",
             pargs: List[Any] = None, executor="default"):
    if executor == "default" or executor == "processpool":
        app.apscheduler.add_job(f, args=pargs, id=task_id,
                                executor=executor,
                                next_run_time=next_tick(wait_before))
    else:
        raise ValueError("Unsupport runner type:%s" % executor)


def cron_task(f, app, default_interval: int, task_id: str = "",
              pargs: List[Any] = None, executor="default"):
    def _f(*args, **kwargs):
        with app.app_context():
            ret = f(*args, **kwargs)
            print("exit call!")
            if ret and isinstance(ret, int):
                if ret == TaskControl.STOP:
                    return
                next_run_time = next_tick(ret)
            else:
                next_run_time = next_tick(default_interval)
            print("re scheduler the job")
            app.apscheduler.add_job(_f, args=pargs,
                                    next_run_time=next_run_time, id=task_id,
                                    executor=executor)
            return ret
    
    if executor == "default":
        app.apscheduler.add_job(_f, args=pargs, id=task_id,
                                next_run_time=next_tick(default_interval),
                                executor=executor)
    elif executor == "processpool":
        app.apscheduler.add_job(f, "interval", args=pargs, id=task_id,
                                executor=executor, seconds=default_interval)
    else:
        raise ValueError("Unsupport runner type:%s" % executor)
