import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.types.password import PasswordType

MAX_GROUP_SIZE = 10

db = SQLAlchemy()


class CourseType(enum.Enum):
    python = "Python"
    vue = "Vue"
    django = "Django"
    php = "PHP"
    html = "HTML"


class GroupStatus(enum.Enum):
    looking_for_applicants = "Looking for applicants"
    applicants_found = "Applicants found"
    in_progress = "In progress"
    archived = "Archived"


class ApplicantStatus(enum.Enum):
    new = "New"
    in_progress = "In progress"
    payment_completed = "Payment completed"
    group_assigned = "Group assigned"


class Applicant(db.Model):
    __tablename__ = 'applicants'
    id = db.Column(db.Integer, primary_key=True, )
    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    group = db.relationship('Group')
    status = db.Column(
        db.Enum(ApplicantStatus,
                values_callable=lambda x: [e.value for e in x]),
        nullable=False)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    status = db.Column(
        db.Enum(GroupStatus,
                values_callable=lambda x: [e.value for e in x]),
        nullable=False)
    course = db.Column(
        db.Enum(CourseType,
                values_callable=lambda x: [e.value for e in x]),
        nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    applicants = db.relationship('Applicant')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(PasswordType(schemes=['pbkdf2_sha512']),
                         nullable=False)
