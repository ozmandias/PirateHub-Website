from flask import redirect, render_template, session
from functools import wraps

def error():
    return render_template("error.html")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
