from functools import wraps
from flask import g, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_context = g.user_context
        if not user_context.is_authenticated:
            return redirect(url_for('redirect.redirect'))
        return f(*args, **kwargs)
    return decorated_function
