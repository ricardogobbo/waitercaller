from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User

DB = DBHelper()

login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = '7C3EFA07EDEDA80D939A595DB7A3872E748784A29804D94A6FE75FBA45D8F8C0'
login_manager.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/account")
@login_required
def account():
    return "You are logged in"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user_password = DB.get_user(email)
    if user_password and user_password == password:
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)