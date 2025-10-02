from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from functools import wraps
from db import (
    init_db_all, create_user, check_login,
    create_project, list_user_projects
)

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
    projects = list_user_projects(current_user_id())
    return render_template("dashboard.html", projects=projects)

@app.route("/project/create", methods=["POST"])
@login_required
def project_create():
    name = request.form.get("name", "").strip() or "New Project"
    pid = create_project(name, current_user_id())
    flash("Project created.", "success")
    return redirect(url_for("dashboard"))

@app.cli.command("init-db")
def init_db_cmd():
    init_db_all()
    print("DB initialized (users + projects). No demo user created.")

if __name__ == "__main__":
    init_db_all()
    app.run(debug=True)
