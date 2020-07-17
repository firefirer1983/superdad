import os
import random
import time

class Pricy:
    
    def __init__(self):
        pass
    
    @staticmethod
    def run(ctx):
        while True:
            print("depth update at %r" % os.getpid())
            curr_depth = ctx.okex.depth
            curr_depth[0][0] = random.random()
            ctx.okex.depth = curr_depth
            # print("depth updated!")
            time.sleep(3)
        # if not self._ws:
        #     self._ws = socketio.Client()
        #     self._ws.connect('http://127.0.0.1:8008')
        # try:
        #     self._ws.emit("post-message", "Hello! I am APScheduler")
        #     print("message emitted!")
        # except Exception as e:
        #     print(e)
        #     self._ws = None
