#!/usr/bin/env python

# Maintained by Marshall Mattingly

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
if __name__ == '__main__':
    print "Running the app",

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atlascms.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
