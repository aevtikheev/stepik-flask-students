import threading

from flask import render_template, request
from flask_mail import Mail, Message

from stepik_p3.app import app
from stepik_p3 import forms


def login_required(f):
    return None


def admin_only(f):
    return None


@app.route('/')
def home_page():
    return None


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
