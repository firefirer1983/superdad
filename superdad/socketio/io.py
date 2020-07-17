from flask_socketio import SocketIO

sio = SocketIO()


@sio.on("connect")
def on_connect():
    sio.emit("message", "connected")


@sio.on('post-message')
def handle_message(message):
    sio.emit("post-message", "Hello from socketio server")
