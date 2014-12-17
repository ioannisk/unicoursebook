from django.shortcuts import render
from courses.models import Course, School, CourseFeedback
from django.views import generic
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from courses.forms import UserForm, CourseFeedbackForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Home page
def index(request):
    return render(request, 'courses/index.html')


# Listing the Schools ordered by title
class SchoolsIndexView(generic.ListView):
    template_name = 'courses/schools_index.html'
    model = School
    context_object_name = 'schools'

    def get_queryset(self):
        return School.objects.order_by('title')


# Displaying the courses that a school have
def school_detail(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    courses = school.course_set.order_by('title')
    context = {'school': school, 'courses': courses}
    return render(request, 'courses/school_detail.html', context)


# Displaying the feedback that a course has received
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # visivle variable allow us not to display feedback that was inappropriate
    course_feedbacks = course.coursefeedback_set.filter(visible=True).order_by('-submission_date')
    context = {'course': course, 'course_feedbacks': course_feedbacks}
    return render(request, 'courses/course_detail.html', context)


# Handles feedback given
@login_required()
def course_feedback(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_feedback_exists = False
    # Check if this user has already submitted a review about the course, if yes she/he can edit it and resubmit
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
        # if user has already submitted a feedback he/she can see it displayed
        if old_feedback:
            course_feedback_form = CourseFeedbackForm(instance=old_feedback.first())
            course_feedback_exists = True
        else:
            course_feedback_form = CourseFeedbackForm()
        context = {'course': course, 'course_feedback_form': course_feedback_form,
                   'course_feedback_exists': course_feedback_exists}
        return render(request, 'courses/course_feedback.html', context)


# Handles Registering process
def user_register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)  # do not yet save in the DB until the password is encrypted
            user.set_password(user.password)    # password encryption
            user.save()
            return HttpResponseRedirect(reverse('courses:index'))
    else:
        user_form = UserForm()

    context = {'user_form': user_form}
    return render(request, 'courses/register.html', context)


# Handles Login
def user_login(request):
    valid = True
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
            valid = False
            context = {'next_url': next_url, 'valid': valid}
            return render(request, 'courses/login.html', context)
    else:
        # parameter 'next' contains the original url in case user tried to access a view that requires authentication
        # we need to propagate 'next' in the login form to redirect the user after login
        # to the page where authentication was required

        next_url = request.GET.get('next')
        if next_url:
            context = {'next_url': next_url, 'valid': valid}
        else:
            context = {}
        return render(request, 'courses/login.html', context)


# Handles Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('courses:index'))