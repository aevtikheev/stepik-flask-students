import threading

from flask import render_template, request, redirect, flash, url_for
from flask_mail import Mail, Message
from flask_login import current_user, login_user, logout_user

from stepik_p3.app import app, login_manager
from stepik_p3 import forms, models


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
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login_page'))
    else:
        return redirect(url_for('admin.index'))


@app.route('/mail')
def mail_page():
    mail_form = forms.MailForm()
    return render_template("mail_edit.html", mail_form=mail_form)


@app.route('/mail_sent', methods=['POST'])
def mail_sent_page():
    recepient = request.form.get('recepient')
    subject = request.form.get('topic')
    text = request.form.get('text')

    mail = Mail(app)
    sender = "user_from@example.com"
    msg = Message(
        subject,
        sender=sender,
        recipients=[recepient]
    )
    msg.body = text

    send_mail_thread = threading.Thread(target=mail.send(msg))
    send_mail_thread.start()

    return render_template("mail_sent.html",
                           recepient=recepient,
                           subject=subject,
                           text=text)
