from flask import Flask,render_template,session,request,redirect,url_for
from flask_socketio import SocketIO,emit,join_room
import secrets
import string
import names
from flask_jsglue import JSGlue

app = Flask(__name__)
jsglue = JSGlue(app)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)
rooms={}
admins = {}

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/game',methods=["POST"])
def index():
    #print(user)
    session['room_name'] = request.form['room_name']
    session['username'] = request.form['user_name']
    print('index',session['room_name'],session['username'])
    return render_template('index.html',data={'room_name':session['room_name'],'user_name':session['username']})

@app.route('/room')
def room():
    print('here',session['room_name'],session['username'])
    return render_template('room.html',rooms=rooms[session['room_name']],room_name=session['room_name'],user_name=session['username'],admins=admins[session['room_name']])

@app.route('/create/<string:user_name>')
def create(user_name):
    res = ''
    while True:
        res = ''
        N = 7
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                      for i in range(N))
        if res not in rooms:
            break
    session['room_name'] = str(res).strip()
    if user_name == "xyzxyz":
        user_name = names.get_first_name().strip()
    session['username']=str(user_name).strip()

    rooms[session['room_name']]=[]
    rooms[session['room_name']].append(session['username'])
    admins[session['room_name']] = session['username']
    return redirect(url_for('room'))

@app.route('/join/<string:user_name>/<string:room_name>')
def join(user_name,room_name):

    session['room_name'] = str(room_name).strip()
    if user_name == "xyzxyz":
        user_name = names.get_first_name().strip()
    session['username']=str(user_name).strip()

    rooms[session['room_name']].append(session['username'])
    return redirect(url_for('room'))



@socketio.on('submit')
def submit(data,room):
    print("In ",room)
    guess = data['guess']
    #print(rooms)
    join_room(session['room_name'])
    emit('announce',{'guess':guess,'user':data['user']},room=room)


@socketio.on('draw_submit')
def draw_submit(data):
    print('here',data['state'])
    print(rooms)
    join_room(session['room_name'])
    emit('draw_announce',{'coord0':data['coord0'],'coord1':data['coord1'],'state':data['state'],'color':data['color'],'thickness':data['thickness']},room=session['room_name'])

@socketio.on('clear_submit')
def clear_submit():
    #print('here',data['state'])
    print(rooms)
    join_room(session['room_name'])
    emit('clear_announce',room=session['room_name'])



@socketio.on('room_joined')
def room_joined(data,room):

    print('room joined')
    join_room(room)
    emit('announce_joined',{'user_name':data['user_name'],'rooms':rooms[session['room_name']]},room=room)


@socketio.on('submit_start_game')
def submit_start_game(data,room):
    #guess = data['guess']
    #print(rooms)
    print('\n'*2)
    print('there','Starting game',session['username'],data['user_name'])
    print('Starting game',data['user_name'],data['room_name'])
    print('\n' * 2)
    session['username'] = data['user_name']
    session['room_name'] = data['room_name']
    join_room(session['room_name'])
    emit('start_game',{'room_name':data['room_name'],'user_name':data['user_name']},room=data['room_name'])


