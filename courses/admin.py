from django.contrib import admin
from courses.models import Course, CourseFeedback, School
from django.forms import Textarea, ModelForm

# model form is needed in order to use text area for comment

class CourseFeedbackModelForm(ModelForm):
    class Meta:
        model = CourseFeedback
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 10}),
        }
        fields = ['course', 'r_course_difficulty', 'r_course_organization', 'r_tutor_presentation', 'r_tutor_support',
                  'r_recommendation', 'visible', 'comment', 'submission_date']


class CourseFeedbackAdmin(admin.ModelAdmin):
    form = CourseFeedbackModelForm
    list_display = ('course', 'comment', 'score', 'submission_date')


class CourseAdmin(admin.ModelAdmin):
    model = Course
    fields = ['school', 'title', 'code', 'url']


admin.site.register(School)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseFeedback, CourseFeedbackAdmin)


