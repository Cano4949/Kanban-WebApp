# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps
from db import init_db_users, create_user, check_login

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret")

def current_user_id():
    return session.get("uid")

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not current_user_id():
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    return redirect(url_for("dashboard") if current_user_id() else url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            flash("Please fill out all fields.", "warning")
            return redirect(url_for("register"))
        uid = create_user(username, password)
        if uid is None:
            flash("Username already taken.", "danger")
            return redirect(url_for("register"))
        session["uid"] = uid
        session["username"] = username
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        uid = check_login(username, password)
        if not uid:
            flash("Invalid credentials.", "danger")
            return redirect(url_for("login"))
        session["uid"] = uid
        session["username"] = username
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.cli.command("init-db")
def init_db_cmd():
    init_db_users()
    print("DB initialized (users).")

if __name__ == "__main__":
    init_db_users()
    app.run(debug=True)
