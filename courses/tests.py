from django.test import TestCase
from courses.models import School, Course, CourseFeedback
from django.core.urlresolvers import reverse


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
        CourseFeedback.objects.create(course=test_course, visible=False, comment='A')
        CourseFeedback.objects.create(course=test_course, visible=True, comment='B')
        response = self.client.get(reverse('courses:course_detail', args=(test_course.id, )))
        self.assertQuerysetEqual(response.context['course_feedbacks'], ['<CourseFeedback: B (0)>'])

    def test_course_detail_if_no_course_feedback(self):
        test_school = School.objects.create(title='TestSchool')
        test_course = Course.objects.create(school=test_school, title='TestCourse')
        response = self.client.get(reverse('courses:course_detail', args=(test_course.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No feedback has been given for this course yet.")
        self.assertQuerysetEqual(response.context['course_feedbacks'], [])
