import uuid
from datetime import datetime

from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.util import NoneType
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, User, db, Note, redis_client
from app.convert import NoteConverter
from app.forms import LoginForm, RegistrationForm, NoteForm


@app.route('/')
@app.route('/index')
def index():
    notes = None
    if current_user.is_authenticated:
        if not redis_client.exists(f'{current_user.id}:notes_id'):
            notes = current_user.notes.order_by(Note.edit_date.desc())
            if notes.count() != 0:
                for note in notes:
                    note_dict = NoteConverter.note_to_dict(note)
                    redis_client.lpush(f'{current_user.id}:notes_id', note_dict['id'])
                    redis_client.hmset(note_dict['id'], note_dict)
                flash('Your notes where loaded from postgresql !', 'info')
            else:
                notes = None
        else:
            notes = []
            count = 0
            while count < redis_client.llen(f'{current_user.id}:notes_id'):
                note_id = redis_client.lindex(f'{current_user.id}:notes_id', count)
                notes.append(NoteConverter.dict_to_note(redis_client.hgetall(note_id)))
                count += 1
            flash('Your notes where loaded from redis !', 'info')
    return render_template("index.html", title='Your notes', notes=notes)


@app.route('/new', methods=['GET', 'POST'])
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
                    uuid=uuid.uuid4())
        # insert into postgresql
        db.session.add(note)
        db.session.flush()
        # get id of inserted note
        db.session.refresh(note)
        db.session.commit()
        # insert into redis
        redis_client.lpush(f'{current_user.id}:notes_id', note.id)
        redis_client.hmset(note.id, NoteConverter.note_to_dict(note))
        flash('Your note has been created !', 'success')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='New note', form=form)


@app.route('/shared/<uuid>')
def shared(uuid):
    note = Note.query.filter_by(uuid=uuid, is_public=True).first()

    if isinstance(note, NoneType):
        flash('This note does not exists !', 'warning')
        return redirect(url_for('index'))

    user = User.query.get(note.id_user)
    return render_template('shared.html', note=note, user=user)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if isinstance(note, NoneType) or current_user.id != note.id_user:
        flash('This note does not exists !', 'warning')
        return redirect(url_for('index'))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        edit_date = datetime.now()
        # update note in postgresql
        note.title = form.title.data
        note.content = form.content.data
        note.is_public = form.is_public.data
        note.edit_date = edit_date
        db.session.commit()
        # update note in redis
        redis_client.hmset(note_id, {'title': form.title.data,
                                     'content': form.content.data,
                                     'is_public': str(form.is_public.data),
                                     'edit_date': str(edit_date)})
        # remove note id from list and re-add it at the start
        redis_client.lrem(f'{current_user.id}:notes_id', 0, str(note.id))
        redis_client.lpush(f'{current_user.id}:notes_id', note.id)
        flash('Your note has been updated !', 'success')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='Update a note', form=form)


@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
@login_required
def delete(note_id):
    note = Note.query.get(note_id)
    if isinstance(note, NoneType) or current_user.id != note.id_user:
        flash('This note does not exists !', 'warning')
    else:
        # remove note from posgres
        db.session.delete(note)
        db.session.commit()
        # remove note from redis
        redis_client.lrem(f'{current_user.id}:notes_id', 0, str(note.id))
        redis_client.delete(str(note.id))
        flash('Your note has been deleted !', 'success')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'warning')
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
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
