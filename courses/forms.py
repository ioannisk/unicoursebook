from courses.models import CourseFeedback
from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ('r_course_difficulty',
                  'r_course_organization','r_tutor_presentation',
                  'r_tutor_support','r_recommendation','comment',)