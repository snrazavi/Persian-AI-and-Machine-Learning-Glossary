from functools import wraps
from flask import request, redirect, url_for
from flask_login import current_user, LoginManager
from admin_user import AdminUser


login_manager = LoginManager()


def admin_required(f):
    """A decorator for the admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for("main.index", next=request.url))
        return f(*args, **kwargs)

    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    """Load user"""
    if user_id == "admin":
        return AdminUser()
    return None
    # return User.query.get(int(user_id))
