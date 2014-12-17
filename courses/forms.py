from courses.models import CourseFeedback
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(validators=[
        RegexValidator(
            regex='ed.ac.uk$',
            message='Email must belong to the ed.ac.uk domain',
            code='invalid_email'
        ), ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # def is_valid(self):
    #     valid = super(UserForm, self).is_valid()
    #     if not valid:
    #         return valid
    #
    #     if not self.fields['email'].endswith('@ed.ac.uk'):
    #         return False
    #
    #     return True


class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ('r_course_difficulty',
                  'r_course_organization','r_tutor_presentation',
                  'r_tutor_support','r_recommendation','comment',)