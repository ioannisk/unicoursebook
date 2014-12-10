from django.conf.urls import patterns, url

from courses import views


urlpatterns = patterns('',
                       url(r'^$', views.SchoolsIndexView.as_view(), name='schools_index'),
                       url(r'^(?P<school_id>\d+)/$', views.school_detail, name='school_detail'),
                       url(r'^courses/(?P<course_id>\d+)/$', views.course_detail, name='course_detail'),
                       url(r'^courses/(?P<course_id>\d+)/feedback/$', views.course_feedback, name='course_feedback'),
                       url(r'^register/$', views.user_register, name='user_register'),
                       url(r'^login/$', views.user_login, name='user_login'),
                       url(r'^logout/$', views.user_logout, name='user_logout'),
)