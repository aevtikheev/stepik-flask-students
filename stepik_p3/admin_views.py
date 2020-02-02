import hashlib

from flask_admin.contrib import sqla


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
