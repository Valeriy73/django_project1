from django.shortcuts import render
from django.http import HttpResponse

# Views for Students
def students_list(request):
    return render(request, 'students/students_list.html', {})

def students_add(request):
    return HttpResponse('<h1>Students ADD Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit students %s</h1>' %sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Students %s</h1>' %sid)

# Views for Groups
def groups_list(request):
    return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
    return HttpResponse('<h1>Group ADD Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' %gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' %gid)


# Create your views here.
