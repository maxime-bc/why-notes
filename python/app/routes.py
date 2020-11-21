import copy
import pprint
import uuid
from datetime import datetime
from typing import Dict, Any

from flask import url_for, render_template, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flask_sqlalchemy import BaseQuery
from sqlalchemy.util import NoneType
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import app, User, db, Note, redis_client
from app.forms import LoginForm, RegistrationForm, NoteForm


class RedisPost(object):
    def __init__(self, dic):
        for k, v in dic.items():
            if not isinstance(k, int):
                var = k.decode()
                setattr(self, var, v.decode())


def decode_dict(dict_to_decode: Dict[Any, Any]) -> Dict[Any, Any]:
    decoded_dict = dict()
    for k, v in dict_to_decode.items():
        if not isinstance(k, int):
            var = k.decode()
            decoded_dict[var] = v.decode()
    return decoded_dict


def redis_add_notes(notes: BaseQuery):
    pp = pprint.PrettyPrinter(indent=4)
    for note in notes:
        note_dict = copy.deepcopy(note.__dict__)
        pp.pprint(note_dict)

        # convert dict values to str
        for key in note_dict:
            note_dict[key] = str(note_dict[key])

        # pp.pprint(note_dict)
        pp.pprint(note_dict)
        note_id = str(note_dict['id'])
        redis_client.rpush('notes_id', note_id)
        redis_client.hmset(note_id, note_dict)


@app.route('/')
@app.route('/index')
def index():
    pp = pprint.PrettyPrinter(indent=4)
    notes = None
    if current_user.is_authenticated:

        if not redis_client.exists('notes_id'):
            print('INSIDE IF !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            notes = current_user.notes.order_by(Note.edit_date.desc())
            redis_add_notes(notes)
        else:
            notes = []
            count = 0
            while count < redis_client.llen('notes_id'):
                note_id = redis_client.lindex('notes_id', count)
                # pp.pprint(redis_client.hgetall(note_id))
                note_dict = decode_dict(redis_client.hgetall(note_id))
                note_dict['id'] = int(note_dict['id'])
                note_dict['creation_date'] = datetime.strptime(note_dict['creation_date'], '%Y-%m-%d %H:%M:%S.%f')
                note_dict['edit_date'] = datetime.strptime(note_dict['edit_date'], '%Y-%m-%d %H:%M:%S.%f')
                note_dict['id_user'] = int(note_dict['id_user'])
                note_dict['is_public'] = bool(note_dict['is_public'])
                note_dict.pop('_sa_instance_state', None)
                pp.pprint(note_dict)
                notes.append(Note(**note_dict))

                # print(type(note_dict))
                # pp.pprint(note_dict)
                # print(note_dict[b'id'])

                # pp.pprint({'test': 'test1'})
                # n = Note(id=note_dict['id'], title=note_dict['title'], content=note_dict['content'])
                # print(n)
                # notes.append(n)
                count += 1

        # print(type(notes))
        # print(notes.column_descriptions())

        # for attr_name in Note.__table__.columns:
        #     for note in notes:
        #         print(attr_name)
        #         print(type(attr_name))
        #         #print(getattr(note, attr_name))
    print(notes)
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
        db.session.add(note)
        db.session.commit()
        flash('Your note has been created !')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='New note', form=form)


@app.route('/shared/<uuid>')
def shared(uuid):
    note = Note.query.filter_by(uuid=uuid, is_public=True).first()

    if isinstance(note, NoneType):
        flash('This note has not been found !')
        return redirect(url_for('index'))

    user = User.query.get(note.id_user)
    return render_template('shared.html', note=note, user=user)


@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit(note_id):
    note = Note.query.filter_by(id=note_id).first()
    if current_user.id != note.id_user:
        flash('You don\'t have the required permissions to access this content !')
        return redirect(url_for('index'))
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.is_public = form.is_public.data
        note.edit_date = datetime.now()
        db.session.commit()
        flash('Your note has been updated !')
        return redirect(url_for('index'))
    return render_template('note_form.html', title='Update a note', form=form)


@app.route('/delete/<int:note_id>', methods=['GET', 'POST'])
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
