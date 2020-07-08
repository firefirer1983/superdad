import time
from functools import wraps
from multiprocessing import Queue
from queue import Empty, Full
from typing import Dict


class Bucket:
    def __init__(self, size, timeout):
        assert size >= 1, "Bucket size must >= 1"
        self._size = size
        self._timeout = timeout
        self._q = Queue(maxsize=self._size)
    
    def is_empty(self):
        return self._q.qsize() == 0
    
    def get(self):
        try:
            ret = self._q.get(timeout=self._timeout)
            print("bucket token:%r" % id(self))
            return ret
        except Empty:
            print("refill bucket:%r for timeout" % id(self))
            for _ in range(self._size - 1):
                self._q.put(id(self))
            return id(self)
    
    def refill(self):
        for _ in range(self._size):
            try:
                self._q.put(id(self))
            except Full:
                break


class TokenBucket:
    def __init__(self, size):
        self._buckets_count = size
        self._buckets: Dict[int, Bucket] = {}
        self._app = None
    
    def init_app(self, app):
        self._app = app
    
    def refill(self):
        print("refill buckets from cron")
        for bucket in self._buckets.values():
            if bucket.is_empty():
                bucket.refill()
    
    def __call__(self, count: int, period: int, interval: int = 0):
        
        def _f(f):
            if len(self._buckets) == self._buckets_count:
                raise RuntimeError("Run out of buckets")
            
            bucket_id = id(f)
            if bucket_id not in self._buckets:
                print("create bucket:%r for %r" % (bucket_id, f))
                self._buckets[bucket_id] = Bucket(
                    size=count,
                    timeout=float(period) / 1000
                )
                self._buckets[bucket_id].refill()
            bucket = self._buckets[bucket_id]
            
            @wraps(f)
            def _wrapper(*args, **kwargs):
                bucket.get()
                with self._app.app_context():
                    ret = f(*args, **kwargs)
                if interval:
                    time.sleep(float(interval) / 1000)
                return ret
            
            return _wrapper
        
        return _f
