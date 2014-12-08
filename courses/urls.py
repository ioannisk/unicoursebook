from django.conf.urls import patterns, url

from courses import views


urlpatterns = patterns('',
    url(r'^$', views.SchoolsIndexView.as_view() , name='schools_index'),
    url(r'^(?P<school_id>\d+)/$', views.school_detail, name='school_detail'),
    url(r'^courses/(?P<course_id>\d+)/$', views.course_detail, name='course_detail'),
    url(r'^courses/(?P<course_id>\d+)/feedback/$', views.course_feedback, name='course_feedback'),
    url(r'^courses/(?P<course_id>\d+)/feedback/submission/$', views.course_feedback_submission, name='course_feedback_submission'),
        )