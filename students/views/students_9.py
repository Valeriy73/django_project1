# -*- coding: utf-8 -*-
from ..models.student import Student
from ..models.group import Group

from django.core.urlresolvers import reverse

from django.shortcuts import render
from django.http import HttpResponseRedirect

from datetime import datetime

def students_edit(request, sid):
    student = Student.objects.get(id=sid)
    groups = Group.objects.all()
    sid1 = {'sid': sid}
    # Если метод POST
    if request.method == "POST":
        # Если кнопка "добавить" была нажата
        if request.POST.get('add_button') is not None:
            errors = {}
            student.middle_name = request.POST.get('middle_name')
            student.notes = request.POST.get('notes')
            # Есть ли пустые строки

            student.first_name = request.POST.get('first_name')
            if not student.first_name.strip():
                errors['first_name'] = u"Це поле потрібно заповнить"

            student.last_name = request.POST.get('last_name')
            if not student.last_name.strip():
                errors['last_name'] = u"Це поле потрібно заповнить"

            student_group = request.POST.get('student_group').strip()
            if not student_group:
                errors['student_group'] = u'Виберіть группу'


            student.birthday = request.POST.get('birthday')
            if not student.birthday.strip():
                errors['birthday'] = u"Це поле потрібно заповнить"
            else:
                try:
                   student.birthday = datetime.strptime(student.birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u'Введіть правильну дату'

            student.ticket = request.POST.get('ticket')
            if not student.ticket.strip():
                errors['ticket'] = u"Вкажіть номер білету"

            student.photo = request.FILES.get('photo')
            if student.photo:
                exe = student.photo.name.split('.')
                if not (exe[1] in ['png', 'gif', 'jpg', 'jpeg']):
                    errors['photo'] = u"Це не формат малюнка"
            # Есть ли не валидные строки

            # Если errors нет сохраняем и переходим назад на вызвавшую страницу
            if not errors:

                student.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_edit1.html',
                              {'errors': errors, 'student': student,
                               'groups': groups, 'sid': sid1})
        # иначе если нажата кнопка "Отменить"
        else:
            # возврат на вызвавшую страницу
            return HttpResponseRedirect(reverse('home'))
    # иначе если метод GET
    else:

        return render(request, 'students/students_edit1.html',
                      {'student': student, 'groups': groups, 'sid': sid1})

        # загружаем страницу с данными для этого пользователя
