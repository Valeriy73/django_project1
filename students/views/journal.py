# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Journal
def journal_list(request):
    return render(request, 'students/journal.html',
                  {})

def journal_stud(request):
    return HttpResponse('<h1>Journal student %s</h1>' %jid)

def journal_update(request, gid):
    return HttpResponse('<h1>Update journal</h1>')
# Create your views here.
