import socketio


class Pricy:
    
    def __init__(self):
        self._ws = None
    
    def run(self):
        if not self._ws:
            self._ws = socketio.Client()
            self._ws.connect('http://localhost:8008')
        try:
            self._ws.emit("post-message", "Hello! I am APScheduler")
        except Exception as e:
            print(e)
            self._ws = None
        print("say hello to you!")
