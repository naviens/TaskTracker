from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from models import TaskGroup, Task, TaskDetail


class TaskGroupTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser('admin', 'admin@example.com',
                                                  'password')
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_001_task_group(self):
        url = reverse('group_list')
        data = {'name': 'Group1', 'description': 'Demo Group'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskGroup.objects.count(), 1)

        # test list groups
        response = self.client.get('/groups/1/')
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'Group1', 'description': 'Demo Group'},
                         msg='list groups failed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test edit groups
        response = self.client.put('/groups/1/',
                                   {'name': 'Group1', 'description': 'Edit Group'})
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'Group1', 'description': 'Edit Group'},
                         msg='edit groups failed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test delete groups
        response = self.client.delete('/groups/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_002_task(self):
        url = reverse('task_list')
        data = {'title': 'Task1', 'description': 'Demo task', 'status': 1, 'created_by': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        # test list tasks
        response = self.client.get('/tasks/1/')
        created_at = response.data['created_at']
        updated_at = response.data['updated_at']
        self.assertEqual(response.data,
                            {'is_completed': False, 'title': u'Task1', 'created_at': created_at,
                             'updated_at': updated_at, 'created_by': u'admin', 'id': 1, 'task_group': None,
                             'task_group_name': None, 'week_hours': None},
                         msg='list tasks failed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # test delete tasks
        response = self.client.delete('/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)