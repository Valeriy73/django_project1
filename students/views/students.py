# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.views.generic import UpdateView, DeleteView, CreateView
from django.forms import ModelForm

from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions


from ..models.student import Student
from ..models.group import Group

# Views for Students
def students_list(request):

    students = Student.objects.all()

    # try to order students list
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()

    # paginate students

    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver
        # last page of results
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html',
                  {'students': students})
"""
def students_add(request):

    # Якщо форма була запощена:
    if request.method == "POST":

        # Якщо кнопка Додати була натиснута:
        if request.POST.get('add_button') is not None:
            # Перевіряємо дані на коректність та збираемо помилки
            errors = {}
            # validate student data will go here
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}

            first_name = request.POST.get('first_name').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name

            last_name = request.POST.get('last_name').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name

            birthday = request.POST.get('birthday').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковим"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday']= u"Введіть коректний формат дати (напр. 1984-12-30)"
                else:
                    data['birthday'] = birthday

            ticket = request.POST.get('ticket').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket

            student_group = request.POST.get('student_group').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) !=1:
                    errors['student-group'] = u"Оберіть коректну групу"
                else:
                    data['student_group'] = groups[0]

            photo = request.FILES.get('photo')
            if photo:
                format_pic = ('jpg', 'jpeg', 'png', 'gif') # кортеж из графических форматов
                if photo.name.lower().endswith(format_pic) == False: #конец строки сравниваем с кортежом
                    errors['photo'] = u'Це не э зображенням!'
                elif photo.size > 2*1024*1024:
                    errors['photo'] = u'Розмір файла повинен бути меньшим ніж 2Мб'
                else:
                    data['photo'] = photo

            # Якщо дані були введені коректно:
                # Створюємо та зберігаємо студента в базу
            if not errors:
                student = Student(**data)
                student.save()
                # Повертаємо користувача до списку студентів
                messages.success(request, u"Студента %s %s успішно додано!" %(data['last_name'], data['first_name']))
                return HttpResponseRedirect(reverse('home'))
            # Якшо дані були введені некоректно:
                # Вшддаємо шаблон форми разом із знайденими помилками
            else:
                return render (request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title'),
                    'errors': errors})
        # Якщо кнопка Скасувати була натиснута:
        elif request.POST.get('cancel_button') is not None:
            # Повертаємо користувача до списку студентів
            messages.warning(request, u'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
    # Якщо форма не була запощена:
        # повертаємо код початкового стану форми
    else:
        return render (request, 'students/students_add.html',
                    {'groups': Group.objects.all().order_by('title')})

    return render(request, 'students/students_add.html',
                  {'groups': Group.objects.all().order_by('title')})

#def students_edit(request, sid):
#
#    return HttpResponse('<h1>Edit students %s</h1>' %sid)"""

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = fields = ['first_name', 'last_name', 'middle_name',
         'birthday', 'photo', 'ticket', 'notes', 'student_group']
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

class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'middle_name',
         'birthday', 'photo', 'ticket', 'notes', 'student_group']

    def __init__(self, *args, **kwargs):
        super(StudentCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('students_add')
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

class StudentCreateView(CreateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentCreateForm

    def get_success_url(self):
        messages.success(self.request, u"Студента успішно додано!")
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Додавання студента відмінено!')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super(StudentCreateView, self).post(request, *args, **kwargs)


class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(self.request, u"Студента успішно збережено!")
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(self.request, u'Редагування студента відмінено!')
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
