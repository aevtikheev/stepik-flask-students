import threading

import flask_mail
from flask import redirect, url_for, flash
from flask_admin.contrib import sqla
from flask_admin import AdminIndexView, BaseView, expose
from flask_login import current_user
from wtforms.fields import PasswordField

from stepik_p3 import models, forms

APPLICANTS_SHOW_AMOUNT = 10
GROUPS_SHOW_AMOUNT = 10

mail = flask_mail.Mail()


class AuthorizationMixIn:
    """ Makes view to require authorization """

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_page'))


class UserModelView(AuthorizationMixIn, sqla.ModelView):
    """ Model view for users """
    column_searchable_list = ('name', 'email')
    column_exclude_list = ['password']
    form_overrides = dict(password=PasswordField)


class GroupModelView(AuthorizationMixIn, sqla.ModelView):
    """ Model view for groups """
    column_formatters = dict(course=lambda v, c, m, p: m.course.value)


class ApplicantsModelView(AuthorizationMixIn, sqla.ModelView):
    """ Model view for applicants """


class DashboardView(AuthorizationMixIn, AdminIndexView):
    @expose('/')
    def index(self):
        total_applicants_count = (
            models.db.session.query(models.Applicant)
            .count()
        )
        new_applicants_count = (
            models.db.session.query(models.Applicant)
            .filter(models.Applicant.status == models.ApplicantStatus.new)
            .count()
        )
        new_applicants_to_show = (
            models.db.session.query(models.Applicant)
            .filter(models.Applicant.status == models.ApplicantStatus.new)
            .limit(APPLICANTS_SHOW_AMOUNT)
        )
        groups = models.db.session.query(models.Group)\
            .limit(GROUPS_SHOW_AMOUNT)
        return self.render('admin/dashboard.html',
                           total_applicants_count=total_applicants_count,
                           new_applicants_count=new_applicants_count,
                           new_applicants=new_applicants_to_show,
                           groups=groups)


class MailView(AuthorizationMixIn, BaseView):
    @expose('/', methods=['GET', 'POST'])
    def mail_page(self):
        mail_form = forms.MailForm()
        mail_form.recepient.choices = [
            (applicant.email, f'{applicant.name}, {applicant.email}')
            for applicant in models.Applicant.query.all()
        ]
        if mail_form.validate_on_submit():
            try:
                _send_mail(recepient=mail_form.recepient,
                           subject=mail_form.subject,
                           text=mail_form.text)
            except Exception as exc:
                print(exc)  # TODO: logging
                flash('Mail wasn\'n sent', category='error')
            else:
                flash('Mail sent', category='success')
        return self.render("admin/mail.html", mail_form=mail_form)


def _send_mail(recepient, subject, text):
    sender = "user_from@example.com"

    msg = flask_mail.Message(
        subject,
        sender=sender,
        recipients=[recepient]
    )
    msg.body = text

    send_mail_thread = threading.Thread(target=mail.send(msg))
    send_mail_thread.start()
