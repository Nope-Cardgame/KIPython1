import socketio
from Connection import sio


# Emitted Events:
def playAction(action):
    sio.emit("playAction", action)

def ready(acceptance):
    sio.emit("ready", acceptance)

# Received Events:
@sio.event
def connect():
    """ Basic SocketIO event raised on connection """
    print("Client connected")

@sio.event
def connect_error(data):
    """ Basic SocketIO event raised on connection error """
    print("Connection failed")

@sio.event
def disconnect():
    """ Basic SocketIO event raised on disconnect """
    print("Client disconnected")

@sio.on("gameState")
def gameState(data):
    pass

@sio.on("error")
def error(data):
    pass

@sio.on("banned")
def banned(data):
    pass

@sio.event
def gameEnd(data):
    pass

@sio.event
def tournamentInvite(data):
    pass

@sio.event
def gameInvite(data):
    pass

