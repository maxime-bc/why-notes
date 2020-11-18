from datetime import datetime

from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, User, db, Note
from app.forms import LoginForm, RegistrationForm, NoteForm


@app.route('/')
@app.route('/index')
def index():

    notes = None
    if current_user.is_authenticated:
        notes = current_user.notes.order_by(Note.edit_date.desc())
        if len(notes.all()) == 0:
            notes = None
    return render_template("index.html", title='Your notes', notes=notes)


@app.route('/new',  methods=['GET', 'POST'])
@login_required
def new():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data,
                    content=form.content.data,
                    creation_date=datetime.now(),
                    edit_date=datetime.now(),
                    author=current_user,
                    is_public=form.is_public.data,
                    uuid='uuid')
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created !')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='New note', form=form)


@app.route('/edit/<int:note_id>',  methods=['GET', 'POST'])
@login_required
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if current_user.id != note.id_user:
        flash('You don\'t have the required permissions to access this content !')
        return redirect(url_for('index'))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        print(note)
        note.title = form.title.data
        note.content = form.content.data
        note.is_public = form.is_public.data
        note.edit_date = datetime.now()
        print(note)
        db.session.commit()
        flash('Your note has been updated !')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='Update a note', form=form)


@app.route('/delete/<int:note_id>',  methods=['GET', 'POST'])
@login_required
def delete(note_id):
    note = Note.query.get(note_id)
    if current_user.id != note.id_user:
        flash('You don\'t have the required permissions to access this content !')
    else:
        db.session.delete(note)
        db.session.commit()
        flash('Your note has been deleted !')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.firstname.data, last_name=form.lastname.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
