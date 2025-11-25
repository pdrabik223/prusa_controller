from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    # Handle incoming message from the client
    print('Received message:', message)
    # Perform necessary actions or send a response

@socketio.on('connect')
def test_connect(auth):
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect(reason):
    print('Client disconnected, reason:', reason)
        
@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    
    
@app.route('/')
def index():
    
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app)