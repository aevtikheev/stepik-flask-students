from flask import Flask
from flask_admin import Admin

from stepik_p3 import models
from stepik_p3 import config
from stepik_p3 import admin_views

app = Flask(__name__)
app.config.from_object(config.Config)
models.db.init_app(app)

with app.app_context():
    models.db.create_all()


admin = Admin(app)
admin.add_view(admin_views.UserView(models.User, models.db.session))
admin.add_view(admin_views.GroupView(models.Group, models.db.session))
admin.add_view(admin_views.ApplicantsView(models.Applicant, models.db.session))


if __name__ == '__main__':
    app.run()
