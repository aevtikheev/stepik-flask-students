from flask import Flask
from flask_admin import Admin

from stepik_flask_students import models, config
from stepik_flask_students.views import admin_views
from stepik_flask_students.views.base_views import login_manager, auth_page


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)
    app.url_map.strict_slashes = False
    models.db.init_app(app)

    login_manager.init_app(app)
    admin_views.mail.init_app(app)

    admin = Admin(app,
                  template_mode='bootstrap3',
                  index_view=admin_views.DashboardView())
    admin.add_view(admin_views.UserModelView(models.User, models.db.session))
    admin.add_view(admin_views.GroupModelView(models.Group, models.db.session))
    admin.add_view(admin_views.ApplicantsModelView(models.Applicant, models.db.session))
    admin.add_view(admin_views.MailView(name="Send e-mail", endpoint='mail'))

    app.register_blueprint(auth_page)

    return app
