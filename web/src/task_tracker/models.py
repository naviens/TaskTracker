from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

# Create your models here.

STATUS_CHOICES = (
    (0, 'New'),
    (1, 'InProgress'),
    (2, 'Completed'),
)


class TaskGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    task_group = models.ForeignKey(TaskGroup, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)


class TaskDetail(models.Model):
    task = models.ForeignKey(Task)
    work_hours = models.SmallIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
