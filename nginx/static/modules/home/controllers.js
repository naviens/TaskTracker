'use strict';

angular.module('Home')

.controller('HomeController',
    ['$scope', '$rootScope', '$location', '$cookieStore' , '$http', 'GroupService', 'TaskService', 'TaskInfoService',
    function ($scope, $rootScope, $location, $cookieStore, $http ,GroupService, TaskService, TaskInfoService) {
        // reset login status
        // TaskService.GetData();

        $scope.init = function () {
            console.log('init ...');
            var glob=$cookieStore.get('globals');
            if(glob.currentUser.token){
                var token = glob.currentUser.token
                console.log(token)
                $http.defaults.headers.common['Authorization'] = 'Token ' + token; // jshint ignore:line
            } else { 
                console.log('Not logged in')
            }
        };

        $scope.getGroups = function () {
            $scope.dataLoading = true;
            $scope.all_groups = [];
            GroupService.getGroups(function (response) {
                /// if response object has auth_token
                $scope.all_groups = response;
            });
            return $scope.all_groups
        };

        $scope.getGroup = function (pk) {
            $scope.dataLoading = true;
            $scope.one_group = '';
            GroupService.getGroup(pk, function (response) {
                $scope.one_group = response;
            });
        };

        $scope.createGroup = function () {
            var data = { name: $scope.group_name, description: $scope.group_desc };
            GroupService.createGroup(data, function (response) {
                if (response) {
                    console.log('Success');
                    $('#createGroupModal').modal('hide');
                } else {
                    $scope.error = response.message;
                    $scope.dataLoading = false;
                }
            });
        };

        $scope.getTasks = function () {
            $scope.dataLoading = true;
            $scope.all_tasks = [];
            TaskService.getTasks(function (response) {
                $scope.all_tasks = response;
            });
        };

        $scope.getTask = function (pk) {
            $scope.dataLoading = true;
            $scope.task_data = '';
            TaskService.getTask(pk, function (response) {
                $scope.task_data = JSON.stringify(response);
            });
        };

        $scope.updateTaskStatus = function (task) {
            
            $scope.dataLoading = true;
            $scope.task_data = '';
            task.is_completed=event.target.checked;
            TaskService.updateTask(task.id, task, function (response) {
                $scope.task_data = JSON.stringify(response);
            });
        };

        $scope.createTask = function () {
            var data = { title: $scope.task_title, task_group: $scope.task_group };
            TaskService.createTask(data, function (response) {
                if (response) {
                    console.log('Success');
                    $('#createTaskModal').modal('hide');
                    $scope.getTasks();

                } else {
                    $scope.error = response.message;
                    $scope.dataLoading = false;
                }
            });
        };

        $scope.deleteTask = function (pk) {
            $scope.dataLoading = true;
            TaskService.deleteTask(pk, function (response) {
                $scope.getTasks();
            });
        };

        $scope.getTasksInfo = function (task_id) {
            $scope.dataLoading = true;
            $scope.all_tasks_info = '';
            $scope.task_id = task_id
            TaskInfoService.getTasksInfo(task_id, function (response) {
                /// if response object has auth_token
                $scope.all_tasks_info = response;
            });
        };

        $scope.deleteTaskInfo = function (task_id, pk) {
            $scope.dataLoading = true;
            TaskInfoService.deleteTaskInfo(task_id, pk, function (response) {
                $scope.getTasksInfo(task_id);
                $scope.getTasks();
            });
        };



        $scope.createTaskInfo = function () {
            var data = { work_hours: $scope.work_hours};
            TaskInfoService.createTaskInfo($scope.task_id, data, function (response) {
                if (response) {
                    console.log('Success'); 
                    $('#createTaskInfoModal').modal('hide');
                    $scope.all_tasks_info.push(response);
                    $scope.getTasks();

                } else {
                    $scope.error = response.message;
                    $scope.dataLoading = false;
                }
            });
        };


    }]);