from flask import Flask, render_template, session, g

app = Flask(__name__)
app.secret_key = 'invalidhelp-secret-key-2024'

from app.pharmacy import bp as pharmacy_bp
app.register_blueprint(pharmacy_bp)

@app.context_processor
def inject_current_user():
    from app.pharmacy import DBStorage, UserItem
    user_id = session.get('user_id')
    if user_id:
        try:
            db = DBStorage()
            user = db.GetUser(user_id)
            db.db.close()
            return {'current_user': user}
        except Exception:
            pass
    return {'current_user': None}

@app.route("/")
def index():
    return render_template("index.tpl")
