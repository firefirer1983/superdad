import socketio
from flask import Flask

from ..ctx import Context
from ..model import Favourite

sio = socketio.Client()


class Depthy:
    def __init__(self, app: Flask = None):
        self._app = app
        self._ctx = app.ctx
        self._connected = False
    
    @property
    def app(self):
        return self._app
    
    def connect(self):
        print("I'm connected!", self._ctx)
    
    def disconnect(self):
        print("I'm disconnected!", self._ctx)
    
    def connect_error(self):
        print("connect error", self._ctx)
    
    def on_depth(self, event, data):
        print("event:", event)
        print("data:", data)
        print(self.ctx)
    
    @property
    def ctx(self) -> Context:
        return self._ctx
    
    def install_event_callback(self):
        sio.event(self.connect)
        sio.event(self.disconnect)
        sio.event(self.connect_error)
        sio.event("depth", self.on_depth)
    
    def run(self):
        sio.sleep(2)
        print("start socketio")
        self.install_event_callback()
        while True:
            
            with self.app.app_context():
                print(Favourite.list_stock())
            if not self._connected:
                try:
                    ret = sio.connect('http://localhost:8008')
                    print("connect:", ret)
                except Exception as e:
                    print(str(e), "connect failed, wait 5s then reconnect")
                    sio.sleep(5)
                    continue
                self._connected = True
            sio.emit("post-message", "Hello from depthy!")
            # d = self.ctx.okex.depth
            sio.sleep(3)
