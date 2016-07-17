# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Віталій',
         'last_name': u'Подоба',
         'ticket': 235,
         'image': 'img/student1.jpg'},
        {'id': 2,
         'first_name': u'Андрій',
         'last_name': u'Короста',
         'ticket': 2123,
         'image': 'img/student2.jpg'},
        {'id': 3,
         'first_name': u'Вареник',
         'last_name': u'Петро',
         'ticket': 5323,
         'image': 'img/student3.jpeg'}
         )
    return render(request, 'students/students_list.html',
                  {'students': students})

def students_add(request):
    return HttpResponse('<h1>Students ADD Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit students %s</h1>' %sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Students %s</h1>' %sid)

# Views for Groups
def groups_list(request):
    groups = (
        {'id': 1,
         'group_name': u'МтМ-21',
         'headman': u'Ячменев Олег'
         },
        {'id': 2,
         'group_name': u'МтМ-22',
         'headman': u'Віталій Подоба'
         },
        {'id': 3,
         'group_name': u'МтМ-23',
         'headman': u'Іванов Андрій'
         }
        )
    return render(request, 'students/groups_list.html',
                  {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group ADD Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' %gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' %gid)

# Views for Journal
def journal_list(request):
    return render(request, 'students/journal.html',
                  {})

def journal_stud(request):
    return HttpResponse('<h1>Journal student %s</h1>' %jid)

def journal_update(request, gid):
    return HttpResponse('<h1>Update journal</h1>')
# Create your views here.
