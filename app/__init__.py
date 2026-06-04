from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'invalidhelp-secret-key-2024'
login_manager = LoginManager(app)
login_manager.login_message = 'Войдите, чтобы открыть эту страницу'

from app.pharmacy import bp as pharmacy_bp
app.register_blueprint(pharmacy_bp)
login_manager.login_view = f'{pharmacy_bp.name}.login'

from app.api import api_bp
app.register_blueprint(api_bp)

@login_manager.user_loader
def load_user(user_id):
    from app.pharmacy import DBStorage
    try:
        db = DBStorage()
        user = db.GetUser(int(user_id))
        db.db.close()
        return user if user.id else None
    except Exception:
        return None

@app.route("/")
def index():
    return render_template("index.tpl")
