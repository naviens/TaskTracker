from rest_framework import serializers
from django.db.models import Sum
import datetime

from models import TaskDetail, TaskGroup, Task


class TaskSerializer(serializers.ModelSerializer):
    task_group_name = serializers.SlugField(source='task_group.name', read_only=True)
    week_hours = serializers.SerializerMethodField()
    created_by = serializers.CharField(required=False)

    def get_week_hours(self, obj):
        # last 7 days
        end_date = datetime.date.today()
        start_date = end_date + datetime.timedelta(days=-7)
        hours = TaskDetail.objects.filter(task=obj.id,
                                          created_at__range=[start_date, end_date]
                                          ).aggregate(Sum('work_hours'))
        return hours['work_hours__sum']

    class Meta:
        model = Task
        fields = ('id', 'title', 'task_group', 'created_by', 'created_at', 'week_hours',
                  'updated_at', 'is_completed', 'task_group_name')


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup


class TaskDetailSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(required=False)
    # task = serializers.RelatedField(source='task', read_only=True)
    task = serializers.ReadOnlyField(source='task.id')

    class Meta:
        model = TaskDetail
