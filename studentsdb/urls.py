"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, url, include
from django.contrib import admin
import students.views.students
import students.views.groups
import students.views.journal
import students.views.contact_admin
from .settings import MEDIA_ROOT, DEBUG
from students.views.students import StudentUpdateView, StudentDeleteView
from students.views.journal import JournalView

urlpatterns = [
    # Students urls
    url(r'^$', students.views.students.students_list, name='home'),
    url(r'^students/add/$', students.views.students.students_add,
        name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(),
        name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', StudentDeleteView.as_view(),
        name='students_delete'),

    # Groups urls
    url(r'^groups/$', students.views.groups.groups_list, name='groups'),
    url(r'^groups/add/$', students.views.groups.groups_add, name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', students.views.groups.groups_edit,
        name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', students.views.groups.groups_delete,
        name='groups_delete'),

    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', JournalView.as_view(), name='journal'),
    #url(r'^journal/(?P<jid>\d+)/$', students.views.journal.journal_stud, name='journal_stud'),
    #url(r'^journal/update', students.views.journal.journal_update, name='journal_update'),

    # Contact Admin Form
    url(r'^contact-admin/$', students.views.contact_admin.contact_admin, name='contact_admin'),

    url(r'^admin/', include(admin.site.urls)),
]

if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT}))
