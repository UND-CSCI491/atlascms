from flask import Flask, Request
import atlascms.configs

def create_app(config=atlascms.configs.ConfigDevelopment):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'SECRETKEY'

    # ensure a graceful exit
    app.teardown_appcontext(shutdown_session)

    # grab our views
    from atlascms.views.frontend import frontend
    from atlascms.views.user import user

    # register our blueprints
    app.register_blueprint(frontend)
    app.register_blueprint(user, url_prefix='/user')

    # return the app
    return app

def shutdown_session(exception=None):
    '''Shutsdown all session-related things.'''
    from atlascms.database import session
    session.close()
