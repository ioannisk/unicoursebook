from django.shortcuts import render
from courses.models import Course, School, CourseFeedback
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from courses.forms import UserForm, UserProfileForm



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
    else:
        return render(request, 'courses/course_feedback.html', context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)  # do not yet save in the DB until the password is encrypted
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 'registered': registered, 'profile_form': profile_form}
    return render(request,
                  'courses/register.html',
                  context,
    )

