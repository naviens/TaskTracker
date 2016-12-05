from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [

    url(r'^groups/$', views.TaskGroupList.as_view(),
        name='group_list'),
    url(r'^groups/(?P<pk>[0-9]+)/$', views.TaskGroupInfo.as_view(),
        name='group_info'),

    url(r'^tasks/$', views.TaskList.as_view(),
        name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskInfo.as_view(),
        name='task_info'),

    url(r'^tasks/(?P<task_id>[0-9]+)/details/$',
        views.TaskDetailList.as_view(),
        name='task_details_list'),
    url(r'^tasks/(?P<task_id>[0-9]+)/details/(?P<pk>[0-9]+)/$',
        views.TaskDetailInfo.as_view(),
        name='task_details_info'),
]

urlpatterns = format_suffix_patterns(urlpatterns)