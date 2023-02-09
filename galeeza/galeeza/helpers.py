import os
from flask import redirect, render_template, request, session
from functools import wraps


# Render message as an apology to user
# code from the Finance exercise
def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Decorate routes to require login - https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
# code from the Finance exercise
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/signup")
        return f(*args, **kwargs)
    return decorated_function

