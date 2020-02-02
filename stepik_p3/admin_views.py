import hashlib

from flask_admin.contrib import sqla
from flask_admin import AdminIndexView, expose

from stepik_p3 import models

APPLICANTS_SHOW_AMOUNT = 10
GROUPS_SHOW_AMOUNT = 10


class UserView(sqla.ModelView):
    """ Model view for users """
    def on_model_change(self, form, model, is_created):
        model.password = hashlib.md5(
            model.password.encode('utf-8')
        ).hexdigest()


class GroupView(sqla.ModelView):
    """ Model view for groups """


class ApplicantsView(sqla.ModelView):
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
        new_applicants = (
            models.db.session.query(models.Applicant)
            .filter(models.Applicant.status == models.ApplicantStatus.new)
            .limit(APPLICANTS_SHOW_AMOUNT)
        )
        groups = models.db.session.query(models.Group)\
            .limit(GROUPS_SHOW_AMOUNT)
        return self.render('admin/dashboard.html',
                           total_applicants_count=total_applicants_count,
                           new_applicants_count=new_applicants_count,
                           new_applicants=new_applicants,
                           groups=groups,
                           max_group_size=models.MAX_GROUP_SIZE)
