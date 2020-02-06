from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     PasswordField,
                     SubmitField,
                     validators)


class MailForm(FlaskForm):
    recepient = StringField(u'Recepient:', [validators.required()])
    subject = StringField(u'Subject:', [validators.required()])
    text = TextAreaField(u'Text:', [validators.required()])


class LoginForm(FlaskForm):
    email = StringField('E-mail', [validators.required()])
    password = PasswordField('Password', [validators.required()])
    submit = SubmitField('Submit')
