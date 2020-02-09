from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user

from stepik_flask_students.app import app, login_manager
from stepik_flask_students import forms, models


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        user = models.User.query.filter_by(email=login_form.email.data).first()
        if user is None or user.password != login_form.password.data:
            flash('Invalid email or password')
            return redirect(url_for('login_page'))
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('auth.html', login_form=login_form)


@app.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login_page'))
    else:
        return redirect(url_for('admin.index'))
