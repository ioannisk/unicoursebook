from django.shortcuts import render
from courses.models import Course, School, CourseFeedback
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class SchoolsIndexView(generic.ListView):
    template_name = 'courses/schools_index.html'
    model = School
    context_object_name = 'schools'

    def get_queryset(self):
        return School.objects.order_by('title')


def school_detail(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    courses = school.course_set.order_by('title')
    context = {'school': school, 'courses': courses}
    return render(request, 'courses/school_detail.html', context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_feedbacks = course.coursefeedback_set.filter(visible=True).order_by('-submission_date')
    context = {'course': course, 'course_feedbacks': course_feedbacks}
    return render(request, 'courses/course_detail.html', context)


def course_feedback(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    if request.method == 'GET':
        return render(request, 'courses/course_feedback.html', context)
    if request.method == 'POST':
        new_feedback = CourseFeedback()
        new_feedback.course_id = course_id
        new_feedback.r_course_difficulty = request.POST['r_course_difficulty']
        new_feedback.r_course_organization = request.POST['r_course_organization']
        new_feedback.r_tutor_presentation = request.POST['r_tutor_presentation']
        new_feedback.r_tutor_support = request.POST['r_tutor_support']
        new_feedback.r_recommendation = request.POST['r_recommendation']
        new_feedback.save()
        return HttpResponseRedirect(reverse('courses:course_detail', args=(course.id,)))



#wrvwrv
# def course_feedback_submission(request, course_id):
#     course = get_object_or_404(Course, pk=course_id)
#     return HttpResponseRedirect(reverse('courses:course_feedback', args=(course.id,)))




