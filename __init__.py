from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email

import Feedback
from forms import CreateFaqForm, CreateFeedbackForm
from Base import *
from datetime import datetime
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session


import shelve, Faq
app = Flask(__name__)

# pip install Flask-WTF


'''class contactForm(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email(granular_message=True)])
    message = StringField(label='Message')
    submit = SubmitField(label="Log In")'''


@app.route('/')
def admin():
    return render_template('admin.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


'''@app.route("/", methods=["GET", "POST"])
def contact():
    cform = contactForm()
    if cform.validate_on_submit():
        print(f"Name:{cform.name.data}, E-mail:{cform.email.data},message: {cform.message.data}")
    return render_template("contact.html", form=cform)'''


@app.route('/createfaq', methods=['GET', 'POST'])
def create_faq():
    create_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and create_faq_form.validate():
        faq_dict = {}
        db = shelve.open('faq.db', 'c')

        try:
            faq_dict = db['FAQ']

        except:
            print("Error in retrieving data")

        faq = Faq.Faq(create_faq_form.question.data, create_faq_form.answer.data)
        faq_dict[faq.get_question_id()] = faq
        db['FAQ'] = faq_dict

        faq_dict = db['FAQ']
        faq = faq_dict[faq.get_question_id()]
        print(faq.get_question(), faq.get_answer(), "was stored in faq.db successfully with id: ", faq.get_question_id())

        db.close()

        return redirect(url_for('admin'))
    return render_template('createfaq.html', form=create_faq_form)


@app.route('/retrievefaq')
def retrieve_faq():
    faq_dict = {}
    db = shelve.open('faq.db', 'r')
    faq_dict = db['FAQ']
    db.close()
    faq_list = []

    for key in faq_dict:
        faq = faq_dict.get(key)

        faq_list.append(faq)
    return render_template('retrievefaq.html', count=len(faq_list), faq_list=faq_list)


@app.route('/updatefaq/<int:id>/', methods=['GET', 'POST'])
def update_faq(id):
    update_faq_form = CreateFaqForm(request.form)
    if request.method == 'POST' and update_faq_form.validate():
        faq_dict = {}
        db = shelve.open('faq.db', 'w')
        faq_dict = db['FAQ']

        faq = faq_dict.get(id)
        faq.set_question(update_faq_form.question.data)
        faq.set_answer(update_faq_form.answer.data)

        db['FAQ'] = faq_dict
        db.close()

        return redirect(url_for('retrieve_faq'))
    else:
        faq_dict = {}
        db = shelve.open('faq.db', 'r')
        faq_dict = db['FAQ']
        db.close()

        faq = faq_dict.get(id)
        update_faq_form.question.data = faq.get_question()
        update_faq_form.answer.data = faq.get_answer()

        return render_template('updatefaq.html', form=update_faq_form)


@app.route('/deletefaq/<int:id>', methods=['POST'])
def delete_faq(id):
    faq_dict = {}
    db = shelve.open('faq.db', 'w')
    faq_dict = db['FAQ']

    faq_dict.pop(id)

    db['FAQ'] = faq_dict
    db.close()

    return redirect(url_for('retrieve_faq'))


@app.route('/createfeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('feedback.db', 'c')

        try:
            feedback_dict = db['Feedback']

        except:
            print("Error in retrieving data")

        feedback = Feedback.Feedback(create_feedback_form.name.data, create_feedback_form.subject.data, create_feedback_form.content.data)
        feedback_dict[feedback.get_feedback_id()] = feedback
        db['Feedback'] = feedback_dict

        feedback_dict = db['Feedback']
        feedback = feedback_dict[feedback.get_feedback_id()]
        print(feedback.get_name(), feedback.get_subject(), feedback.get_content(), "was stored in feedback.db successfully with id: ", feedback.get_feedback_id())

        db.close()

        return redirect(url_for('admin'))
    return render_template('createfeedback.html', form=create_feedback_form)


@app.route('/retrievefeedback')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('feedback.db', 'r')
    feedback_dict = db['Feedback']
    db.close()
    feedback_list = []

    for key in feedback_dict:
        feedback = feedback_dict.get(key)

        feedback_list.append(feedback)
    return render_template('retrievefeedback.html', count=len(feedback_list), feedback_list=feedback_list)


@app.route('/deletefeedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('feedback.db', 'w')
    feedback_dict = db['Feedback']

    feedback_dict.pop(id)

    db['Feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)
'''

'''app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'''

Session(app)

socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method=='POST'):
        username = request.form['username']
        room = request.form['room']
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session = session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app)

if __name__ == "__main__":
    app.run()
