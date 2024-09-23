from flask import (Flask, g, jsonify, redirect, render_template, request,
                   session)
from passlib.hash import pbkdf2_sha256



from db import Database

DATABASE_PATH = 'flashrewind.db'

app = Flask(__name__)
app.secret_key = b'demokeynotreal!'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database(DATABASE_PATH)
    return db

@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/subjects')
def subjects():
    return render_template('subjects.html')





@app.route('/my_subjects')
def my_subjects():
    return render_template('my_subjects.html')

@app.route('/subject/<int:subject_id>/notes/')
def view_subject_notes(subject_id):
    subject_details = get_db().get_subject(subject_id)

    subject_notes = get_db().get_subject_notes(subject_id)
    if subject_details:
        return render_template('subject_notes.html', subject=subject_details, notes=subject_notes)
    else:
        return render_template('404.html')


@app.route('/subject/<int:subject_id>/createnotes/', methods=['POST'])
def create_subject_notes(subject_id):
    subject_details = get_db().get_subject(subject_id)
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        get_db().create_subject_notes(question, answer, subject_id)

    if subject_details:
        return redirect(f"/subject/{subject_id}/notes/", code=302)

@app.route('/subject/<int:subject_id>/note/<int:note_id>/delete/')
def delete_note(subject_id, note_id):
    print('innnnnn', request.method)
    note = get_db().delete_note(note_id)
    return redirect(f"/subject/{subject_id}/notes/", code=302)

@app.route('/flash_cards/<int:subject_id>')
def get_flashcards(subject_id):
    subject_details = get_db().get_subject(subject_id)
    subject_notes = get_db().get_subject_notes(subject_id)
    print(subject_notes)
    if subject_details:
        return render_template('flashcard.html', subject=subject_details, notes=subject_notes)
    else:
        return render_template('404.html')
    

def generate_get_subjects_response(args):
    user_id = session['user']['id']
    return jsonify({
        'subjects': get_db().get_user_subjects(user_id),
        'total': get_db().get_user_num_subjects(user_id)
    })

@app.route('/api/user/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    if request.method == 'DELETE':
        subject = get_db().delete_subject(subject_id)
        print('hereee')
        return render_template('my_subjects.html')
    


@app.route('/api/user/subjects', methods=['GET','POST', 'DELETE'])
def user_home():
    message = None
    if request.method == 'POST':
        subject_name = request.form.get('subject')
        subject_description = request.form.get('description')
        print(subject_name, subject_description)
        if subject_name:
            if 'user' in session:
                user_id = session['user']['id']
                subject = get_db().create_subject(subject_name, subject_description,  user_id, 1)
                return render_template('my_subjects.html')
        else:
            message = "Please provide subject name."
            
    elif request.method == "GET":
        print("getmethod")
        if 'user' in session:
            return generate_get_subjects_response(request.args)
        
    return render_template('my_subjects.html')

@app.route('/login', methods=['GET','POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form['email']
        typed_password = request.form['password']
        print(email)
        print(typed_password)
        if email and typed_password:
            user = get_db().get_user(email)
            print('********************')
            print(user)
            if user:
                if pbkdf2_sha256.verify(typed_password, user['password']):
                    session['user'] = user
                    return redirect('/my_subjects')
                else:
                    message = "Incorrect password, please try again"
            else:
                message = "Unknown user, please try again"
        elif email and not typed_password:
            message = "Missing password, please try again"
        elif not email and typed_password:
            message = "Missing username, please try again"
    return render_template('login.html', message=message)

@app.route('/signup',methods=['GET','POST'])
def signup():
    print(request.data)
    if request.method == 'POST':
        print("request", request)
        name = request.form.get('name')
        print(name)
        email = request.form.get('email')
        typed_password = request.form.get('password')
        if name and email and typed_password:
            encrypted_password = pbkdf2_sha256.hash(typed_password)
            get_db().create_user(name, email, encrypted_password)
            return redirect('/login')
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/reset')
def reset():
    return render_template('reset.html')








if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
