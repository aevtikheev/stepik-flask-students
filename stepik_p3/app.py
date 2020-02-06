from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager

from stepik_p3 import models, config, admin_views

app = Flask(__name__)
app.config.from_object(config.Config)
models.db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
admin_views.mail.init_app(app)

admin = Admin(app,
              template_mode='bootstrap3',
              index_view=admin_views.DashboardView())
admin.add_view(admin_views.UserModelView(models.User, models.db.session))
admin.add_view(admin_views.GroupModelView(models.Group, models.db.session))
admin.add_view(admin_views.ApplicantsModelView(models.Applicant,
                                               models.db.session))
admin.add_view(admin_views.MailView(name="Send e-mail", endpoint='/mail'))


from stepik_p3.views import *  # TODO use blueprints

if __name__ == '__main__':
    app.run()
