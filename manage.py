#!/usr/bin/env python

import os, subprocess, sys

# global variables
base = os.path.dirname(os.path.realpath(__file__))
env  = os.path.join(base, 'env')

def create_env():
    '''Creates our virtual environment.'''
    # see if it's already been created
    if os.path.exists(env):
        return True

    # try to create it
    virtualenv = os.path.join(base, 'virtualenv-1.11.4', 'virtualenv.py')
    if 0 != subprocess.call(['python', virtualenv, 'env']):
        print 'Unable to create env. Please delete env folder and try again.'
        return False

    # setup our virtual environment
    pip = os.path.join(env, 'bin', 'pip')
    if not os.path.exists(pip):
        pip = os.path.join(env, 'Scripts', 'pip.exe')
        if not os.path.exists(pip):
            print 'Unable to find pip executable. Make sure env was created.'
            return False

    # install our requirements
    if 0 != subprocess.call([pip, 'install', '-r', 'requirements.txt']):
        print 'Issues install our requirements. Please check output.'
        return False

    # we did it all!
    return True

# we do all this outside of main, because yolo

# make sure that our environment is created
if not create_env():
    print 'Unable to create virtual environment!'
    sys.exit(1)

# determine the virtual python executable
INTERP = os.path.join(env, 'bin', 'python')
if not os.path.exists(INTERP):
    INTERP = os.path.join(env, 'Scripts', 'python.exe')

# ensure we found it
if not os.path.exists(INTERP):
    print 'Unable to determine virtual python executable location.'
    sys.exit(1)

# run the process from the virtual python env
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# update the sys path
sys.path.insert(0, base)

# run the app
from flask.ext.script import Manager, prompt_bool, Server, Shell
from atlascms import create_app
application = create_app()
manager = Manager(application)

from atlascms.database import engine, Base, session
import atlascms.models

# commands
manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host = '0.0.0.0')
)

def _make_context():
    return dict(app=application, session=session, metadata=Base.metadata, engine=engine)

manager.add_command('shell', Shell(make_context=_make_context))

# all our commands
@manager.command
def dropdb(force=False):
    '''Drops the entire database.'''
    if force or prompt_bool('Are you sure you want to lose all the data?'):
        Base.metadata.drop_all()

@manager.command
def initdb(force=False):
    '''Initializes the database.'''
    if force or prompt_bool('Delete any existing database?'):
        dropdb(True)
    Base.metadata.create_all()

@manager.command
def unittest():
    '''Performs all of our unit testing.'''
    # destroy and unittest.db and create a new one

@manager.command
def testdata():
    '''Initializes the database with testing data.'''
    from atlascms.models import League, User, Sport, LeagueUserAssociation, \
                                 Team, Game
    initdb(force=True)

    # add 10 users first
    users = []
    for i in range(10):
        username = 'user%d' % (i+1)
        email = '%s@test.com' % username
        user = User(email=email, username=username, password='password')
        users.append(user)
        conf = user.get_confirmation()
        session.add(user)
        session.add(conf)
        session.commit()

if __name__ == '__main__':
    manager.run()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
