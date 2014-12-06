from django.conf.urls import patterns, url

from courses import views


urlpatterns = patterns('',
    url(r'^$', views.SchoolsIndexView.as_view() , name='schools_index'),
    url(r'^(?P<school_id>\d+)/$', views.school_detail, name='school_detail'),
    )