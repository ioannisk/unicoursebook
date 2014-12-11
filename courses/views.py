from django.shortcuts import render
from courses.models import Course, School, CourseFeedback
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from courses.forms import UserForm, UserProfileForm, CourseFeedbackForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'courses/index.html')

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


@login_required()
def course_feedback(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_feedback_exists = False
    old_feedback = CourseFeedback.objects.filter(user=request.user.id, course=course_id)
    if request.method == 'POST':
        if old_feedback:
            course_feedback_form = CourseFeedbackForm(data=request.POST, instance=old_feedback.first())
        else:
            course_feedback_form = CourseFeedbackForm(data=request.POST)
        if course_feedback_form.is_valid():
            new_feedback = course_feedback_form.save(commit=False)
            new_feedback.course = course
            new_feedback.user = request.user
            new_feedback.save()
            return HttpResponseRedirect(reverse('courses:school_detail', args=(course.school_id,)))
        else:
            return HttpResponseBadRequest()
    else:
        if old_feedback:
            course_feedback_form = CourseFeedbackForm(instance=old_feedback.first())
            course_feedback_exists = True
        else:
            course_feedback_form = CourseFeedbackForm()
        context = {'course': course, 'course_feedback_form': course_feedback_form,
                   'course_feedback_exists': course_feedback_exists}
        return render(request, 'courses/course_feedback.html', context)


def user_register(request):

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
            return HttpResponseRedirect(reverse('courses:index'))
        else:
            return HttpResponseBadRequest()
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request,
                  'courses/register.html',
                  context,
    )


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next_url')  # see comment about next_url below
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('courses:schools_index'))
            else:
                return HttpResponse("Your unicoursebook account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        # parameter 'next' contains the original url in case user tried to access a view that requires authentication
        # we need to propagate 'next' in the login form to redirect the user after login
        # to the page where authentication was required

        next_url = request.GET.get('next')
        if next_url:
            context = {'next_url': next_url}
        else:
            context = {}
        return render(request, 'courses/login.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))