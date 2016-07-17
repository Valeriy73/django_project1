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
