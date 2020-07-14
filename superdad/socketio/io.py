from flask_socketio import SocketIO

ws = SocketIO()


@ws.on("connect")
def on_connect():
    ws.emit("message", "connected")


@ws.on('post-message')
def handle_message(message):
    print('received message: ' + message)
