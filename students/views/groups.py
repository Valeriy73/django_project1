# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from django.contrib import messages

from django.views.generic.edit import DeleteView

from ..models.group import Group

from django.db.models import ProtectedError

# Views for Groups
def groups_list(request):
    groups = Group.objects.all()
    # try to order groups list
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    
    #paginate groups
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        #If page is out of range (e.g. 9999), deliver
        #last page of results
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html',
                  {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group ADD Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' %gid)

#def groups_delete(request, gid):
#    return HttpResponse('<h1>Delete Group %s</h1>' %gid)
class GpoupsDelete(DeleteView):
    model = Group
    template_name = "students/group_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            messages.warning(self.request, u"Группу %s не можна видалити, так як до ней ще належать студенти" % self.object)
            return HttpResponseRedirect(reverse("groups"))
        else:
            messages.success(self.request, u"Группа %s успішно видалено!" % self.object)
        return HttpResponseRedirect(reverse("groups"))
