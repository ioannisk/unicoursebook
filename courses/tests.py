from django.test import TestCase
from courses.models import School, Course
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
        Course.objects.create(title='B', code='b', school=test_school)
        Course.objects.create(title='A', code='a', school=test_school)
        response = self.client.get(reverse('courses:school_detail', args=(test_school.id,)))
        self.assertQuerysetEqual(response.context['courses'], ['<Course: A (a)>', '<Course: B (b)>'])

    def test_school_detail_if_no_courses(self):
        test_school = School.objects.create(title='TestSchool')
        response = self.client.get(reverse('courses:school_detail', args=(test_school.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No courses have been defined for this school.")
        self.assertQuerysetEqual(response.context['courses'], [])