from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import serializers
from models import TaskGroup, Task, TaskDetail


class TaskGroupList(generics.ListCreateAPIView):
    """
    URL: /groups/
        Returns a list of all task groups.
        creating new task groups.

    Actions:
        GET:
            - Returns task groups in the system as list
        POST:
            - Creates new task groups with valid attributes
    """
    queryset = TaskGroup.objects.all()
    serializer_class = serializers.TaskGroupSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class TaskGroupInfo(generics.RetrieveUpdateDestroyAPIView):
    """
    URL: /groups/{id}
        Returns a single task group.
        Also allows updating and deleting task group.

    Actions:
        GET:
            - Returns requested task group object.
        PUT:
            - Updates requested task group object.
        DELETE:
            - Deletes requested task group object.
    """
    queryset = TaskGroup.objects.all()
    serializer_class = serializers.TaskGroupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.get(pk=self.kwargs['pk'])
        return self.queryset

    def get_object(self, *args, **kwargs):
        try:
            return self.get_queryset()
        except TaskGroup.DoesNotExist:
            raise NotFound(detail=None)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.serializer_class(group, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskList(generics.ListCreateAPIView):
    """
    URL: /tasks/
        Returns a list of all tasks.
        creating new tasks.

    Actions:
        GET:
            - Returns tasks in the system as list
        POST:
            - Creates new tasks with valid attributes
    """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class TaskInfo(generics.RetrieveUpdateDestroyAPIView):
    """
    URL: /tasks/{id}
        Returns a single task.
        Also allows updating and deleting task.

    Actions:
        GET:
            - Returns requested task object.
        PUT:
            - Updates requested task object.
        DELETE:
            - Deletes requested task object.
    """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.get(pk=self.kwargs['pk'])
        return self.queryset

    def get_object(self, *args, **kwargs):
        try:
            return self.get_queryset()
        except Task.DoesNotExist:
            raise NotFound(detail=None)

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.serializer_class(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskDetailList(generics.ListCreateAPIView):
    """
    URL: /tasks/{id}/details/
        Returns a list of all tasks details for given task.
        creating new task detail.

    Actions:
        GET:
            - Returns task detail for give task in the system as list
        POST:
            - Creates new task detail with valid attributes
    """
    queryset = TaskDetail.objects.all()
    serializer_class = serializers.TaskDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.filter(task=self.kwargs['task_id'])
        return self.queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['task_id'] = self.kwargs['task_id']
            serializer.validated_data['created_by'] = request.user
            serializer.save()
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)


class TaskDetailInfo(generics.RetrieveUpdateDestroyAPIView):
    """
    URL: /tasks/{task_id}/details/{id}
        Returns a single task detail.
        Also allows updating and deleting task detail.

    Actions:
        GET:
            - Returns requested task detail object.
        PUT:
            - Updates requested task detail object.
        DELETE:
            - Deletes requested task detail object.
    """
    queryset = TaskDetail.objects.all()
    serializer_class = serializers.TaskDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Url Filters
        self.queryset = self.queryset.filter(task=self.kwargs['task_id'])
        self.queryset = self.queryset.get(pk=self.kwargs['pk'])
        return self.queryset

    def get_object(self, *args, **kwargs):
        try:
            return self.get_queryset()
        except TaskDetail.DoesNotExist:
            raise NotFound(detail=None)

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.serializer_class(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        task_detail = self.get_object()
        task_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
