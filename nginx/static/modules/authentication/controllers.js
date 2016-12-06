'use strict';

angular.module('Authentication')

.controller('LoginController',
    ['$scope', '$rootScope', '$location', 'AuthenticationService',
    function ($scope, $rootScope, $location, AuthenticationService) {
        // reset login status
        AuthenticationService.ClearCredentials();

        $scope.login = function () {
            $scope.dataLoading = true;
            AuthenticationService.Login($scope.username, $scope.password, function (response) {
                /// if response object has auth_token
                if (response.auth_token) {
                    AuthenticationService.SetCredentials($scope.username, response.auth_token);
                    $location.path('/');
                } else {
                    $scope.error = response.message;
                    $scope.dataLoading = false;
                }
            });
        };

        $scope.logout = function () {
            $scope.dataLoading = true;
            AuthenticationService.Logout(function () {
                $location.path('/login');
            });
        };
    }]);