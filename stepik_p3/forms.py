from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators


class MailForm(FlaskForm):
    recepient = StringField(u'Recepient:', [validators.required()])
    subject = StringField(u'Subject:', [validators.required()])
    text = TextAreaField(u'Text:', [validators.required()])
