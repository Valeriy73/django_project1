# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Journal
def journal_list(request):
    journal = (
        {'id': 1,
         'name': u'Подоба Віталій'},
         {'id': 2,
         'name': u'Корост Андрій'},
         {'id': 3,
         'name': u'Притула Тарас'}
    )
    return render(request, 'students/journal.html',
                  {'journal': journal})

def journal_stud(request, jid):
    return HttpResponse('<h1>Journal student %s</h1>' %jid)

def journal_update(request):
    return HttpResponse('<h1>Update journal</h1>')
# Create your views here.
