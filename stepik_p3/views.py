from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from stepik_p3.app import app
from stepik_p3.models import User
from stepik_p3.forms import LoginForm, RegistrationForm, ChangePasswordForm


def login_required(f):
    return None


def admin_only(f):
    return None


@app.route('/')
@login_required
def home():
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    return None


@app.route('/logout', methods=["POST"])
@login_required
def logout():
    return None


@app.route("/register", methods=["GET", "POST"])
@admin_only
@login_required
def register():
    return None


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    return None
