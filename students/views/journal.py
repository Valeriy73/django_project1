# -*- coding: utf-8 -*-

from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from calendar import monthrange, weekday, day_abbr

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

from ..models.student import Student
from ..models.monthjournal import MonthJournal
from ..util import paginate

from django.http import JsonResponse


class JournalView(TemplateView):
    template_name = 'students/journal.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        # prepare student, dates and presence data
        current_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        month = date(current_date.year, current_date.month, 1)
        present = data['present'] and True or False
        student = Student.objects.get(pk=data['pk'])

        # get or create journal objaect for given student and month
        journal = MonthJournal.objects.get_or_create(student=student, date=month)[0]

        # set new presence on journal for given student and save result
        setattr(journal, 'present_day%d' % current_date.day, present)
        journal.save()

        # return success status
        return JsonResponse({'status': 'success'})


    def get_context_data(self, **kwargs):
        # get context data from TemplateView class
        context = super(JournalView, self).get_context_data(**kwargs)

        # check if we need to display some specific month
        if self.request.GET.get('month'):
            month = datetime.strptime(self.request.GET['month'], '%Y\
-%m-%d'
                ).date()
        else:
            #otherwise just displaying current data
            today = datetime.today()
            month = date(today.year, today.month, 1)

        # обчислюємо поточний рік, попередній і наступний місяці
        # we need this for month navigation element in template
        next_month = month + relativedelta(months=1)
        prev_month = month - relativedelta(months=1)
        context['prev_month'] = prev_month.strftime('%Y-%m-%d')
        context['next_month'] = next_month.strftime('%Y-%m-%d')
        context['year'] = month.year
        context['month_verbose'] = month.strftime('%B')
        # количество записей в журнале студентов с данной датой
        number_row = Student.objects.all().count()
        number_page = number_row//10+1
        first_diap = 0
        end_diap = 9


        # we'll use this variable in students pagination
        context['cur_month'] = month.strftime('%Y-%m-%d')

        # prepare variable for template to generate
        # journal table header elements
        myear, mmonth = month.year, month.month
        number_of_days = monthrange(myear, mmonth)[1]
        context['month_header'] = [{'day': d,
            'verbose': day_abbr[weekday(myear, mmonth, d)][:2]}
            for d in range(1, number_of_days+1)]

        # Отримуємо номер сторінки, разраховуємо діапазон
        if self.request.GET.get("page"):
            page = int(self.request.GET.get("page"))
            first_diap += (page-1)*10
            end_diap = page*10 if (page != number_page) else number_row
        else:
            end_diap = end_diap if number_row//10 else number_row%10


        # get all students from database, or just one if we need to
        # display journal for one student
        if kwargs.get('pk'):
            queryset = [Student.objects.get(pk=kwargs['pk'])]
        else:
            queryset = Student.objects.all().order_by('last_name')[first_diap:end_diap]

        # url to update student presence, for form post
        update_url = reverse('journal')
        # пробігаємось по усіх студентах і збираємо
        # необхідні дані:
        students = []
        for student in queryset:
            # try to get journal object by month selected
            # month and current student
            try:
                journal = MonthJournal.objects.get(student=student, date=month)

            except Exception:
                journal = None

            # fill in days presence list for current student
            days = []
            for day in range(1, number_of_days+1):
                days.append({
                    'day': day,
                    'present': journal and getattr(journal, 'present\
_day%d' %
                        day, False) or False,
                    'date': date(myear, mmonth, day).strftime(
                        '%Y-%m-%d'),
                })

                # набиваэмо усі решту даних студента
            students.append({
                'fullname': u'%s %s' % (student.last_name, student.first_name),
                'days': days,
                'id': student.id,
                'update_url': update_url,
            })


                # застосовуємо пагінацію, 10 студентов на страницеів
        context = paginate(Student.objects.all(), 10, self.request, context,
                    var_name='students')
        context['students'] = students


                # повертаємо оновлений словник із даними
        return context
