from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*')

users = {}

@app.route('/')
def index():
    return "WebSocket server is running..."

@app.route('/websocket/namespace1/message4')
def namespace1_message4():
    # sid = request.sid     # 一般API不可以call request.sid
    socketio.emit('message4', "namespace1 Test message4 by socketio.emit", namespace="/namespace1")     #  不會是廣播, 只有打這支API的client才會收到訊息
    # emit('message4', "namespace1 Test message4 by emit", namespace="/namespace1")         #   這行會掛掉
    return "/websocket/namespace1/message4"


@socketio.on('connect')
def client_connect():
    print("Default namespace socket connected... {0}".format(request.sid))
    emit('connect_response', 'default namespace Connected')
    

@socketio.on('disconnect')
def client_disconnect():
    print("Default namespace socket disconnected... {0}".format(request.sid))


@socketio.on('connect', namespace='/namespace1')
def namespace1_connect():
    print("namespace1 socket connected... {0}".format(request.sid))
    emit('connect_response', 'namespace1 Connected')

@socketio.on('disconnect', namespace='/namespace1')
def namespace1_disconnect():
    print("namespace1 socket disconnected... {0}".format(request.sid))

# Room的event name不一定要用 'join_room', 可以是任何自定義的名子, 官網上是'join'
@socketio.on('join_room', namespace='/namespace1')
def on_join(data):
    print("someone joined the room")
    print("data: ", data)

    sid = request.sid
    ip = request.remote_addr
    username = data['username']
    room = data['room']
    users[ip] = room
    # users[ip] = sid

    # Method1: 如果不用sid當作room name, 就必須要使用join_room()函數
    join_room(room)
    send(username + ' has entered the room.', room=room)

    # Method2: 如果用sid當作room name, 就不用join_room()函數
    # send(username + ' has entered the room.', room=sid)
    print("username: ", username, "room: ", room, "sid: ", sid, "ip: ", ip)



# Room的event name不一定要用 'leave_room', 可以是任何自定義的名子, 官網上是'leave'
@socketio.on('leave_room', namespace='/namespace1')
def on_leave(data):
    print("someone left the room")
    print("data: ", data)

    sid = request.sid
    ip = request.remote_addr
    username = data['username']
    room = data['room']
    users.pop(ip, None)

    send(username + ' has left the room.', room=room)
    leave_room(room)
    

@app.route('/websocket/room/room1')
def namespace1_room1():

    print("someone sent message to the room1")

    # sid = request.sid
    ip = request.remote_addr
    room = users[ip]

    print("room: ", room, "ip: ", ip)

    # socketio.emit('chatroom_msg', "namespace1 room1 message", room=room)                              # 需要指定namespace，否則將傳送失敗
    socketio.emit('chatroom_msg', "namespace1 room1 message", namespace="/namespace1", room=room)     
    # socketio.send("namespace1 room1 message", namespace="/namespace1", room=room)                     # 這個也可以

    return "/websocket/room/room1"


@socketio.on('message')
def default_namespace_receive_message(payload):
    print("default message request.sid: {0}".format(request.sid))
    print('received message: {}'.format(payload))
    
    emit('message', "default namespace Test message")


@socketio.on('message', namespace='/namespace1')
def namespace1_receive_message(payload):
    print("message1 request.sid: {0}".format(request.sid))
    print('received message1: {}'.format(payload))
    
    emit('message', "namespace1 Test message1 Broadcast", broadcast=True)


@socketio.on('message2', namespace='/namespace1')
def namespace1_receive_message2(payload):
    print("message2 request.sid: {0}".format(request.sid))
    print('received message2: {}'.format(payload))

    emit('message2', "namespace1 Test message2", namespace="/namespace1")

@socketio.on('message3', namespace='/namespace1')
def namespace1_receive_message3(payload):
    print("message3 request.sid: {0}".format(request.sid))
    print('received message3: {}'.format(payload))

    socketio.emit('message3', "namespace1 Test message3", namespace="/namespace1")


if __name__ == '__main__':
    print("socket server is running on port 5002")
    socketio.run(app, host="0.0.0.0", port=5002, debug=True)