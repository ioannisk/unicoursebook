from django.test import TestCase
from courses.models import School, Course, CourseFeedback, User
from django.core.urlresolvers import reverse
from django.utils import timezone
import datetime
from django.http import HttpResponseBadRequest


class SchoolViewTest(TestCase):
    def test_school_index_ordering(self):
        School.objects.create(title='B')
        School.objects.create(title='A')
        response = self.client.get(reverse('courses:schools_index'))
        self.assertQuerysetEqual(response.context['schools'], ['<School: A>', '<School: B>'])

    def test_school_index_if_no_schools(self):
        response = self.client.get(reverse('courses:schools_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No schools have been defined.")
        self.assertQuerysetEqual(response.context['schools'], [])

    def test_school_detail_ordering(self):
        test_school = School.objects.create(title='TestSchool')
        Course.objects.create(school=test_school, title='B', code='b')
        Course.objects.create(school=test_school, title='A', code='a')
        response = self.client.get(reverse('courses:school_detail', args=(test_school.id,)))
        self.assertQuerysetEqual(response.context['courses'], ['<Course: A (a)>', '<Course: B (b)>'])

    def test_school_detail_if_no_courses(self):
        test_school = School.objects.create(title='TestSchool')
        response = self.client.get(reverse('courses:school_detail', args=(test_school.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No courses have been defined for this school.")
        self.assertQuerysetEqual(response.context['courses'], [])


class CourseViewTest(TestCase):
    def test_not_visible_feedback_is_not_displayed(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        test_user_1 = User.objects.create_user(username='TestUser1')
        test_user_2 = User.objects.create_user(username='TestUser2')
        CourseFeedback.objects.create(course=test_course, user=test_user_1, visible=False, comment='A')
        CourseFeedback.objects.create(course=test_course, user=test_user_2, visible=True, comment='B')
        response = self.client.get(reverse('courses:course_detail', args=(test_course.id, )))
        self.assertQuerysetEqual(response.context['course_feedbacks'], ['<CourseFeedback: B (0)>'])

    def test_course_detail_if_no_course_feedback(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        response = self.client.get(reverse('courses:course_detail', args=(test_course.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No feedback has been given for this course yet.")
        self.assertQuerysetEqual(response.context['course_feedbacks'], [])

    def test_course_detail_ordering(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse', code='test')
        test_user_1 = User.objects.create_user(username='TestUser1')
        test_user_2 = User.objects.create_user(username='TestUser2')
        new_time = timezone.now()
        old_time = timezone.now() - datetime.timedelta(days=30)
        CourseFeedback.objects.create(course=test_course, user=test_user_1, submission_date=new_time, comment='newer')
        CourseFeedback.objects.create(course=test_course, user=test_user_2, submission_date=old_time, comment='older')
        response = self.client.get(reverse('courses:course_detail', args=(test_course.id,)))
        self.assertQuerysetEqual(response.context['course_feedbacks'],
                                 ['<CourseFeedback: newer (0)>', '<CourseFeedback: older (0)>'])


class CourseFeedbackViewTest(TestCase):
    def test_anonymous_cannot_submit_feedback(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        response = self.client.get(reverse('courses:course_feedback', args=(test_course.id,)))
        # we need to hardcode the url because of the 'next' parameter. See views.user_login for  explanation of 'next'
        self.assertRedirects(response, 'ucb/login/?next=/ucb/courses/%d/feedback/' % test_course.id)

    def test_user_can_submit_feedback(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        test_user = User.objects.create_user(username='TestUser', password='secret')
        self.assertTrue(self.client.login(username=test_user.username, password='secret'))
        payload = {'r_course_difficulty': CourseFeedback.CHOICE_4,
                   'r_course_organization': CourseFeedback.CHOICE_4,
                   'r_tutor_presentation': CourseFeedback.CHOICE_4,
                   'r_tutor_support': CourseFeedback.CHOICE_4,
                   'r_recommendation': CourseFeedback.CHOICE_4,
                   'comment': 'test'}
        response = self.client.post(reverse('courses:course_feedback', args=(test_course.id,)), payload)
        self.assertRedirects(response, reverse('courses:school_detail', args=(test_school.id, )))
        qs = CourseFeedback.objects.filter(user=test_user, course=test_course)
        # 5 is the score that we expect if all choices are CHOICE_4, see models.py for more
        self.assertEqual(qs.first().score(), 5)

    def test_user_can_update_feedback(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        test_user = User.objects.create_user(username='TestUser', password='secret')
        CourseFeedback.objects.create(course=test_course, user=test_user, comment='old')
        self.assertTrue(self.client.login(username=test_user.username, password='secret'))
        payload = {'r_course_difficulty': CourseFeedback.CHOICE_4,
                   'r_course_organization': CourseFeedback.CHOICE_4,
                   'r_tutor_presentation': CourseFeedback.CHOICE_4,
                   'r_tutor_support': CourseFeedback.CHOICE_4,
                   'r_recommendation': CourseFeedback.CHOICE_4,
                   'comment': 'new'}
        response = self.client.post(reverse('courses:course_feedback', args=(test_course.id,)), payload)
        self.assertRedirects(response, reverse('courses:school_detail', args=(test_school.id, )))
        qs = CourseFeedback.objects.filter(user=test_user, course=test_course)
        self.assertEqual(qs.first().comment, 'new')

    def test_incomplete_feedback_is_rejected(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        test_user = User.objects.create_user(username='TestUser', password='secret')
        CourseFeedback.objects.create(course=test_course, user=test_user, comment='old')
        self.assertTrue(self.client.login(username=test_user.username, password='secret'))
        incomplete_payload = {'comment': 'Incomplete'}
        response = self.client.post(reverse('courses:course_feedback', args=(test_course.id,)), incomplete_payload)
        self.assertEqual(response.status_code, HttpResponseBadRequest.status_code)