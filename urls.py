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
#room_name = ''
@app.route('/')
def home():

    return render_template('home.html')

@app.route('/<string:room>')
def index(room):
    print('template',session['room_name'],session['username'])
    return render_template('index.html',data={'room_name':session['room_name'],'user_name':session['username']})

@app.route('/create/<string:user_name>')
def create(user_name):
    N = 7
    res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                  for i in range(N))
    session['room_name'] = str(res)
    if user_name == "xyzxyz":
        user_name = names.get_first_name()
    session['username']=str(user_name)
    print(user_name)
    return redirect(url_for('index',room=res))

@app.route('/join/<string:user_name>/<string:room_name>')
def join(user_name,room_name):

    session['room_name'] = room_name
    if user_name == "xyzxyz":
        user_name = names.get_first_name()
    session['username']=str(user_name)
    print(user_name)
    return redirect(url_for('index',room=room_name))



@socketio.on('submit')
def submit(data,room):
    guess = data['guess']

    join_room(session['room_name'])
    emit('announce',{'guess':guess,'user':data['user']},room=session['room_name'])


@socketio.on('draw_submit')
def draw_submit(data):
    print('here',data['state'])
    #join_room(session['room_name'])
    emit('draw_announce',{'coord0':data['coord0'],'coord1':data['coord1'],'state':data['state'],'color':data['color'],'thickness':data['thickness']},room=session['room_name'])


