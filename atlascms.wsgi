# add this folder to the syspath
import sys, os
DIRNAME = os.path.abspath (os.path.dirname (__file__))
sys.path.insert (0, DIRNAME)
sys.path.append ('/usr/local/lib/python2.7/site-packages')

# create our application
from atlascms import create_app
application = create_app()

if __name__ == '__main__':
    application.run()
