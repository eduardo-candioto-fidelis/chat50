from flask import Flask, render_template, request, jsonify, session, redirect
from flask_socketio import SocketIO, join_room, leave_room
from time import sleep


app = Flask(__name__)
app.config['SECRET_KEY'] = 'banana'
socketio = SocketIO(app)

users_rooms = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        users_rooms[username] = {'talkingwith': None, 'sid': None}
        session['username'] = username

        return redirect('/choose')
        
    return render_template('index.html')


@app.route('/choose', methods=['GET', 'POST'])
def choose():
    return render_template('choose-user.html')


@socketio.on('getuser')
def get_user(json, method=['POST', 'GET']):
    requester_user = session['username']
    requested_user = json['username']
    
    print('user: ' + requester_user)
    print('user: ' + requested_user)

    if requester_user not in users_rooms or requested_user not in users_rooms:
        print('nao encontrado')
        socketio.emit('getuser', 'notfound', room=request.sid)

    elif users_rooms[requested_user]['talkingwith'] == requester_user:
        users_rooms[requester_user]['talkingwith'] = requested_user
        socketio.emit('getuser', 'redirect', room=request.sid)
        
    elif users_rooms[requested_user]['talkingwith'] != None:
        print('Ocupado')
        socketio.emit('getuser', 'occupied', room=request.sid)

    else:
        users_rooms[requester_user]['talkingwith'] = requested_user
        socketio.emit('getuser', 'wait', room=request.sid)

        while True:
            if users_rooms[requested_user]['talkingwith'] == requester_user:
                print('Chat iniciado')
                socketio.emit('getuser', 'redirect', room=request.sid)
                break

            elif users_rooms[requested_user]['talkingwith'] != None:
                print('Ocupado')
                socketio.emit('getuser', 'occupied', room=request.sid)

            else:
                sleep(1)


@app.route('/chat')
def chat():
    actual_user = session['username']
    other_user = users_rooms[actual_user]['talkingwith']

    return render_template('chat.html', username=other_user)


@socketio.on('joining')
def joining(method=['GET', 'POST']):
    actual_user = session['username']
    other_user = users_rooms[actual_user]['talkingwith']
    print('other user: ', other_user)
    print('actual user: ', actual_user)

    users_rooms[other_user]['sid'] = request.sid
    

@socketio.on('chating')
def chating(message, method=['GET', 'POST']):
    print('chating: ', users_rooms)

    user = session['username']
    other_room = users_rooms[user]['sid']

    socketio.emit('chating', message, room=other_room)


@socketio.on('disconnect')
def disconnect():
    user = session['username']

    if user in users_rooms:
        del users_rooms[user]
        print('desconectado...')
    


if __name__ == '__main__':
    socketio.run(app, debug=True)