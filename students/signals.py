# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models.student import Student
from .models.group import Group


@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    """ Writes information about newly added or updated
     student into log file """
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)", student.first_name,
                    student.last_name, student.id)
    else:
        logger.info("Student updated: %s %s (ID: %d)", student.first_name,
                    student.last_name, student.id)


@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):
    """ Writes information about deleted student into log file """
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)", student.first_name,
                student.last_name, student.id)


@receiver(post_save, sender=Group)
def log_group_updated_added_event(sender, **kwargs):
    """ Writes information about newly added or updated
     group into log file """
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group added: %s (ID: %d)", group.title,
                    group.id)
    else:
        logger.info("Group updater: %s (ID: %d)", group.title,
                    group.id)


@receiver(post_delete, sender=Group)
def log_group_delete_event(sender, **kwargs):
    """ Writes information about newly delete group into log file """
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    logger.info("Group delete: %s (ID: %d)", group.title,
                group.id)
