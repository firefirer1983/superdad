from contextlib import contextmanager
from multiprocessing import Semaphore
from multiprocessing.shared_memory import SharedMemory

import numpy as np

OKEX_DEPTH_LEVEL = 5000


@contextmanager
def sem_ctx(sem: Semaphore):
    sem.acquire()
    yield
    sem.release()


class Exchange:
    
    def __init__(self, name, depth_level):
        print("new exchange %s" % name)
        self._sem = Semaphore(1)
        self._name = name
        self._depth_level = depth_level
        self._depth_nbytes = np.ndarray((self._depth_level, 2),
                                        dtype=float).nbytes
        self._depth_shm = SharedMemory(size=self._depth_nbytes,
                                       name="%s.depth" % name,
                                       create=True)
        self._depth = np.ndarray((self._depth_level, 2), dtype=float,
                                 buffer=self._depth_shm.buf)
    
    @property
    def depth_level(self):
        return self._depth_level
    
    @property
    def depth(self):
        with sem_ctx(self._sem):
            ret = np.ndarray(self._depth.shape, dtype=float)
            ret[:] = self._depth[:]
            return ret
        
    @depth.setter
    def depth(self, data):
        if not isinstance(data, np.ndarray):
            raise ValueError("Not valid format:%r" % data)
        with sem_ctx(self._sem):
            self._depth[:] = data[:]


class Context:
    
    def __init__(self):
        self._okex = Exchange("okex", OKEX_DEPTH_LEVEL)
        self._huobi = Exchange("huobi", 150)
    
    @property
    def okex(self):
        return self._okex
    
    @property
    def huobi(self):
        return self._huobi


if __name__ == '__main__':
    ctx = Context()
    ctx.okex.depth = np.ndarray((OKEX_DEPTH_LEVEL, 2), dtype=float)
