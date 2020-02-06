from flask import redirect, url_for
from flask_admin.contrib import sqla
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from wtforms.fields import PasswordField

from stepik_p3 import models

APPLICANTS_SHOW_AMOUNT = 10
GROUPS_SHOW_AMOUNT = 10


class ProtectedView(sqla.ModelView):
    """ Base Model view for authorization-requiring pages """

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_page'))


class UserView(ProtectedView):
    """ Model view for users """
    searchable_columns = ('name', 'email')
    excluded_list_columns = ['password']
    form_overrides = dict(password=PasswordField)


class GroupView(ProtectedView):
    """ Model view for groups """
    column_formatters = dict(course=lambda v, c, m, p: m.course.value)


class ApplicantsView(ProtectedView):
    """ Model view for applicants """


class DashboardView(AdminIndexView):
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
                           groups=groups,
                           max_group_size=models.MAX_GROUP_SIZE)

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_page'))
