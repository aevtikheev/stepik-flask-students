from flask import render_template, redirect, flash, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, LoginManager

from stepik_flask_students import forms, models


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


auth_page = Blueprint('auth_page',
                      __name__,
                      template_folder='templates')


@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.index'))
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        user = models.User.query.filter_by(email=login_form.email.data).first()
        if user is None or user.password != login_form.password.data:
            flash('Invalid email or password')
            return redirect(url_for('.login'))
        login_user(user)
        return redirect(url_for('admin.index'))
    return render_template('auth.html', login_form=login_form)


@auth_page.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@auth_page.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('.login'))
