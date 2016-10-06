# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.group import Group

# Views for Groups
def groups_list(request):
    groups = Group.objects.all()
    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    return render(request, 'students/groups_list.html',
                  {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group ADD Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' %gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' %gid)