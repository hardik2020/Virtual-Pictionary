from flask import Flask,render_template,session,request,redirect,url_for
from flask_socketio import SocketIO,emit,join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)
#room_name = ''
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        session['room_name'] = request.form['room_name']
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/chat')
def index():

    room_name = session['room_name']

    return render_template('index.html',room_name=session['room_name'])

@socketio.on('submit')
def submit(data,room):
    guess = data['guess']

    join_room(session['room_name'])
    emit('announce',{'guess':guess},room=session['room_name'])

@socketio.on('draw_submit')
def draw_submit(data):
    print('here',data['state'])
    #join_room(session['room_name'])
    emit('draw_announce',{'coord0':data['coord0'],'coord1':data['coord1'],'state':data['state'],'color':data['color'],'thickness':data['thickness']},room=session['room_name'])
