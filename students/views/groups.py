# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


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