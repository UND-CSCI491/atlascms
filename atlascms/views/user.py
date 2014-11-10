from flask import Blueprint, current_app, render_template, abort, jsonify, request, redirect, url_for, flash
from atlascms.models import User
from atlascms.database import session
from atlascms.views.session import *

# create our frontend blueprint
user = Blueprint('user', __name__)

@user.route('/')
def index():
    if request.args.get('r') in ['home', 'dashboard', 'user']:
        flash(request.args.get('r'))
        return redirect(request.base_url)

    if is_logged_in():
        try:
            return redirect(url_for('.show', username=get_logged_in_user().username))
        except:
            abort(404)
    abort(404)

@user.route('/signout')
def signout():
    if is_logged_in():
        return jsonify(success=(not set_logged_in(logged_in=False)))
    return jsonify(success=0, message='Not logged in.')

@user.route('/signin', methods=['GET', 'POST'])
def signin():
    if is_logged_in():
        return jsonify(success=0, message='Already logged in.')

    data = {'username': True, 'password': True}
    try:
        data = data_from_request(data)
    except:
        return jsonify(success=0, message='Missing data.')

    # create the user
    user = session.query(User).filter_by(username=data['username'], password=data['password']).first()

    if not user:
        return jsonify(success=0, message='Username or password incorrect.')

    set_logged_in(user_id=user.id, logged_in=True)
    return jsonify(success=1)

@user.route('/new', methods=['GET', 'POST'])
def new():
    if is_logged_in():
        return jsonify(success=0, message='Already signed in.')

    data = {'email': True, 'username': True, 'password': True}
    try:
        data = data_from_request(data)
    except:
        return jsonify(success=0, message='Missing data.')

    # create the user
    user = User(email=data['email'], username=data['username'], password=data['password'])
    conf = user.get_confirmation()
    try:
        session.add(user)
        session.add(conf)
        session.commit()
    except:
        session.rollback()
        return jsonify(success=0, message='Failed to create user.')

    set_logged_in(user_id=user.id, logged_in=True)
    return jsonify(success=1)

@user.route('/<string:username>')
def show(username):
    if request.args.get('r') in ['home', 'dashboard', 'user']:
        flash(request.args.get('r'))
        return redirect(request.base_url)

    if not is_logged_in():
        abort(404)

    usr = session.query(User).filter_by(username=username.replace('-', ' ')).first()
    if not usr:
        abort(404)
    return render_template('user.html',user=usr)

@user.route('/<string:username>/pull')
def pull(username):
    if not is_logged_in():
        abort(404)

    usr = session.query(User).filter_by(username=username).first()
    if not usr:
        abort(404)

    return jsonify(id=usr.id,
                   username=usr.username,
                   name=usr.name,
                   email=usr.email)
