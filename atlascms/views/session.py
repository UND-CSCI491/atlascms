from flask import session as fsession, request
from atlascms.database import session
from atlascms.models import User

def is_logged_in():
    '''Says if we are logged in.'''
    try:
        return fsession['logged_in'];
    except:
        return False

def get_logged_in_user():
    '''Gets the currently logged in user.'''
    if is_logged_in():
        return session.query(User).filter_by(id=fsession['user_id']).first()
    return None

def set_logged_in(user_id = None, logged_in = True):
    '''Sets our logged in state.'''
    if logged_in and user_id:
        fsession['user_id'] = user_id
        fsession['logged_in'] = True
    else:
        fsession['logged_in'] = False
        fsession['user_id'] = 0

    return fsession['logged_in']

def data_from_request(dic):
    if request.method == 'GET':
        for key in dic:
            try:
                dic[key] = request.args.get(key)
            except:
                if dic[key]:
                    raise
                dic[key] = None
    if request.method == 'POST':
        if request.json:
            for key in dic:
                try:
                    dic[key] = request.json[key]
                except:
                    if dic[key]:
                        raise
                    dic[key] = None
        else:
            for key in dic:
                try:
                    dic[key] = request.form[key]
                except:
                    if dic[key]:
                        raise
                    dic[key] = None

    return dic
