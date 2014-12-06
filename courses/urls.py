from django.conf.urls import patterns, url

from courses import views


urlpatterns = patterns('',
    url(r'^$', views.SchoolsIndexView.as_view() , name='schools_index'),
    url(r'^(?P<pk>\d+)/$', views.SchoolDetailView.as_view(), name='school_detail'),
    )