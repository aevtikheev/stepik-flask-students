"""
Script that generates fake data in the DB.
Creates few random users, groups, and applicants(assigned to created groups).
"""
import random
import logging

import faker

from stepik_flask_students.app import create_app
from stepik_flask_students import models

USER_AMOUNT = 3
APPLICANTS_AMOUNT = 10
GROUPS_AMOUNT = 5

logging.basicConfig(filename='db.log', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _create_users(amount):
    fake = faker.Faker()
    for _ in range(amount):
        password = fake.word()
        user = models.User(email=fake.email(),
                           name=fake.name(),
                           password=password)
        models.db.session.add(user)
        logger.info(f'New user {user.email}:{password}')
    models.db.session.commit()
    return [user.id for user in models.db.session.query(models.User).all()]


def _create_groups(amount):
    fake = faker.Faker()
    for _ in range(amount):
        course = random.choice([course.value for course in models.CourseType])
        group = models.Group(
            title=f'{course} {random.randint(1, 1000)}',
            status=random.choice(
                [status.value for status in models.GroupStatus]),
            course=course,
            start_date=fake.date_this_year(),
            max_size=10
        )
        models.db.session.add(group)
        logger.info(f'New group {group.title}')
    models.db.session.commit()
    return [group.id for group in models.db.session.query(models.Group).all()]


def _create_applicants(amount, available_group_ids):
    fake = faker.Faker()
    for _ in range(amount):
        applicant = models.Applicant(
            email=fake.email(),
            phone=fake.phone_number(),
            name=fake.name(),
            group_id=random.choice(available_group_ids),
            status=random.choice(
                [status.value for status in models.ApplicantStatus])
        )
        models.db.session.add(applicant)
        logger.info(f'New applicant: {applicant.name}')
    models.db.session.commit()
    return [applicant.id for applicant in
            models.db.session.query(models.Applicant).all()]


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        models.db.create_all()
        _create_users(USER_AMOUNT)
        group_ids = _create_groups(GROUPS_AMOUNT)
        _create_applicants(APPLICANTS_AMOUNT, group_ids)
