# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.views.generic.edit import UpdateView, DeleteView
from django.forms import ModelForm

from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models.student import Student
from ..models.group import Group

from django import forms



class StudentUpdateForm(forms.Form):
    first_name = forms.CharField(label=u"Ім'я", max_length=128)
    last_name = forms.CharField(label="Прізвище", max_length=128)
    middle_name = forms.CharField(label="По-бфтькові", max_length=128)
    birthday = forms.DateField(input_formats='%Y-%m-%d', label="Дата народження")
    photo = forms.CharField(label=u"Фото", max_length=128)
    ticket = forms.IntegerField(label=u"Білет", max_length=6)
    notes = forms.CharField(label=u"Додаткові нотатки", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout[-1] = FormActions(
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            Submit('cancel_button', u'Скасувати', css_class="btn btn-link"),
            )

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(request, u"Студента успішно збережено!")
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, u'Редагування студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentUpdateView, self).post(request, *args, **kwargs)



#def students_delete(request, sid):
#    return HttpResponse('<h1>Delete Students %s</h1>' %sid)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, u"Студента успішно видалено!")
        return reverse('home')
