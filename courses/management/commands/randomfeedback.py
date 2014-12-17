from django.core.management.base import BaseCommand
from courses.models import Course, CourseFeedback, User
from random import choice, randint
from loremipsum import get_paragraph


def add_users():
    for i in range(50):
        User.objects.create(username="user_%d" %i, password="secret")


class Command(BaseCommand):
    def handle(self, *args, **options):
        add_users()
        users = User.objects.filter(username__startswith="user_")
        courses = Course.objects.all()
        for user in users:
            for course in courses:
                CourseFeedback.objects.create(course=course, user=user, comment=get_paragraph(),
                                              r_course_difficulty=choice([5, 2, 0, -2, -5]),
                                              r_course_organization=choice([5, 2, 0, -2, -5]),
                                              r_tutor_presentation=choice([5, 2, 0, -2, -5]),
                                              r_tutor_support=choice([5, 2, 0, -2, -5]),
                                              r_recommendation=choice([5, 2, 0, -2, -5]),
                                              )

