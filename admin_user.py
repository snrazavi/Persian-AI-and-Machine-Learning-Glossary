"""Admin user class for flask-login."""
from flask_login import UserMixin


class AdminUser(UserMixin):
    """Admin user class for flask-login."""
    id = "admin"
