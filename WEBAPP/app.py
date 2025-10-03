# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import os
from functools import wraps
from db import (
    init_db_all, create_user, check_login,
    create_project, list_user_projects, get_project,
    is_member, add_member, project_members,
    list_columns, create_column, rename_column, delete_column,
    list_cards_by_column, create_card, update_card, delete_card, move_card, is_owner, delete_project
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
    create_project(name, current_user_id())
    flash("Project created.", "success")
    return redirect(url_for("dashboard"))

@app.route("/project/<int:project_id>")
@login_required
def project_view(project_id):
    if not is_member(current_user_id(), project_id):
        abort(403)
    project = get_project(project_id)
    members = project_members(project_id)
    columns = list_columns(project_id)
    cards_by_col = list_cards_by_column(project_id)
    return render_template("project.html", project=project, members=members, columns=columns, cards_by_col=cards_by_col)

@app.route("/project/<int:project_id>/members/add", methods=["POST"])
@login_required
def add_member_route(project_id):
    if not is_member(current_user_id(), project_id):
        abort(403)
    username = request.form["username"].strip()
    if add_member(project_id, username):
        flash("Member added.", "success")
    else:
        flash("User not found.", "warning")
    return redirect(url_for("project_view", project_id=project_id))

@app.route("/column/create", methods=["POST"])
@login_required
def column_create_route():
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    name = request.form.get("name", "").strip() or "New Column"
    create_column(pid, name)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/column/<int:column_id>/rename", methods=["POST"])
@login_required
def column_rename_route(column_id):
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    name = request.form.get("name", "").strip() or "Column"
    rename_column(column_id, name)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/column/<int:column_id>/delete", methods=["POST"])
@login_required
def column_delete_route(column_id):
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    delete_column(column_id)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/card/create", methods=["POST"])
@login_required
def card_create_route():
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    col_id = int(request.form["column_id"])
    title = request.form.get("title", "").strip() or "New Card"
    desc = request.form.get("description", "").strip()
    assignee_id = request.form.get("assignee_id")
    assignee_id = int(assignee_id) if assignee_id else None
    create_card(col_id, title, desc, assignee_id)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/card/<int:card_id>/edit", methods=["POST"])
@login_required
def card_edit_route(card_id):
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    title = request.form.get("title", "").strip() or "Card"
    desc = request.form.get("description", "").strip()
    assignee_id = request.form.get("assignee_id")
    assignee_id = int(assignee_id) if assignee_id else None
    update_card(card_id, title, desc, assignee_id)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/card/<int:card_id>/delete", methods=["POST"])
@login_required
def card_delete_route(card_id):
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    delete_card(card_id)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/card/<int:card_id>/move", methods=["POST"])
@login_required
def card_move_route(card_id):
    pid = int(request.form["project_id"])
    if not is_member(current_user_id(), pid): abort(403)
    to_col = int(request.form["to_column_id"])
    move_card(card_id, to_col)
    return redirect(url_for("project_view", project_id=pid))

@app.route("/project/<int:project_id>/delete", methods=["POST"])
@login_required
def project_delete(project_id):
    if not is_member(current_user_id(), project_id):
        abort(403)
    if not is_owner(current_user_id(), project_id):
        abort(403)
    delete_project(project_id)
    flash("Project deleted.", "success")
    return redirect(url_for("dashboard"))


@app.cli.command("init-db")
def init_db_cmd():
    init_db_all()
    print("DB initialized (users, projects, columns, cards). No demo user created.")

if __name__ == "__main__":
    init_db_all()
    app.run(debug=True)
