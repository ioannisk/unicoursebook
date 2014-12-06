from django.shortcuts import render
from courses.models import Course, School
from django.views import generic


class SchoolsIndexView(generic.ListView):
    template_name = 'courses/schools_index.html'
    model = School
    context_object_name = 'schools'

    def get_queryset(self):
        return School.objects.order_by('title')


class SchoolDetailView(generic.DetailView):
    template_name = 'courses/school_detail.html'
    model = School

    def courses(self):
        return Course.objects.order_by('title')