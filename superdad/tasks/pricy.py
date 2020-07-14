import socketio


class Pricy:
    
    def __init__(self):
        self._ws = None
    
    def run(self):
        if not self._ws:
            self._ws = socketio.Client()
            self._ws.connect('http://localhost:8008')
        self._ws.emit("post-message", "hello")
        print("say hello to you!")
