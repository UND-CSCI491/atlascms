from flask import Blueprint, current_app, render_template, abort, request, redirect, url_for, flash
from atlascms.views.session import *

# create our frontend blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    if request.args.get('r') in ['home', 'dashboard', 'user']:
        flash(request.args.get('r'))
        return redirect(request.base_url)

    if is_logged_in():
        return redirect(url_for('.dashboard'))
    return render_template('home.html')

@frontend.route('/dashboard')
def dashboard():
    if request.args.get('r') in ['home', 'dashboard', 'user']:
        flash(request.args.get('r'))
        return redirect(request.base_url)

    if is_logged_in():
        try:
            user = get_logged_in_user()
            return render_template('dashboard.html', user=user)
        except:
            abort(404)
    return abort(404)
