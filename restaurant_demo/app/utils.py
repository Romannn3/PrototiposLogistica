from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def roles_accepted(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def escape_like_pattern(text):
    if not text:
        return text
    return text.replace('%', '\\%').replace('_', '\\_')
