'use strict';

angular.module('Authentication')

.factory('AuthenticationService',
    ['Base64', '$http', '$cookieStore', '$rootScope', '$timeout',
    function (Base64, $http, $cookieStore, $rootScope, $timeout) {
        var service = {};
        var host_url = 'http://127.0.0.1:8000';

        service.Login = function (username, password, callback) {

            /* Dummy authentication for testing, uses $timeout to simulate api call
             ----------------------------------------------*/
            // $timeout(function () {
            //     var response = { success: username === 'test' && password === 'test' };
            //     if (!response.success) {
            //         response.message = 'Username or password is incorrect';
            //     }
            //     callback(response);
            // }, 1000);

            console.log(username +','+password);
            /* Use this for real authentication
             ----------------------------------------------*/
            // console.log($http.defaults.headers.common);

            $http.post(host_url+'/auth/login/', { username: username, password: password })
               .success(function (response) {
                    console.log(response);
                   callback(response);
               });

        };

        service.Logout = function (callback) {
            $rootScope.globals = {};
            $cookieStore.remove('globals');

            callback();

        };


        service.SetCredentials = function (username, token) {

            $rootScope.globals = {
                currentUser: {
                    username: username,
                    token: token
                }
            };

            
            $cookieStore.put('globals', $rootScope.globals);

            var glob=$cookieStore.get('globals');
            if(glob.currentUser.token){
                $http.defaults.headers.common['Authorization'] = 'Token ' + token; // jshint ignore:line
            } else { 
                console.log('Not logged in')
            }

            console.log(glob)
        };

        service.ClearCredentials = function () {
            $rootScope.globals = {};
            $cookieStore.remove('globals');
            // $http.defaults.headers.common.Authorization = 'Basic ';
        };

        return service;
    }])

.factory('GroupService',
    ['$http',function ($http) {
        var service = {};
        var host_url = 'http://127.0.0.1:8000';

        service.getGroups = function(callback){

            $http.get(host_url+'/groups/')
               .success(function (response) {

                   callback(response['results']);
            });


        };

        service.getGroup = function(pk,callback){
            $http.get(host_url+'/groups/'+ pk +'/')
               .success(function (response) {

                   callback(response);
            });
        };

        service.createGroup = function(data, callback){
            $http.post(host_url+'/groups/', data)
               .success(function (response) {

                   callback(response);
            });
        };

        return service;
    }])


.factory('TaskService',
    ['$http',function ($http) {
        var service = {};
        var host_url = 'http://127.0.0.1:8000';

        service.getTasks = function(callback){

            $http.get(host_url+'/tasks/')
               .success(function (response) {

                   callback(response['results']);
            });
        };

        service.getTask = function(pk,callback){
            $http.get(host_url+'/tasks/'+ pk +'/')
               .success(function (response) {
                   callback(response);
            });
        };

        service.createTask = function(data, callback){
            $http.post(host_url+'/tasks/', data)
               .success(function (response) {

                   callback(response);
            });
        };

        service.updateTask = function(pk, data, callback){
            $http.put(host_url+'/tasks/'+ pk +'/', data)
               .success(function (response) {

                   callback(response);
            });
        };
        service.deleteTask = function(pk,callback){
            $http.delete(host_url+'/tasks/'+ pk +'/')
               .success(function (response) {
                    console.log('success');

                   callback(response);
            });
        };

        return service;
    }])

.factory('TaskInfoService',
    ['$http',function ($http) {
        var service = {};
        var host_url = 'http://127.0.0.1:8000';

        service.getTasksInfo = function(task_id, callback){
            var url = host_url+'/tasks/'+ task_id +'/details/';
            $http.get(url)
               .success(function (response) {

                   callback(response['results']);
            });


        };


        service.deleteTaskInfo = function(task_id, pk,callback){
            $http.delete(host_url+'/tasks/'+ task_id +'/details/'+ pk +'/')
               .success(function (response) {
                    console.log('success');

                   callback(response);
            });
        };

        service.createTaskInfo = function(task_id, data, callback){
            $http.post(host_url+'/tasks/'+ task_id +'/details/', data)
               .success(function (response) {

                   callback(response);
            });
        };

        return service;
    }])

.factory('Base64', function () {
    /* jshint ignore:start */

    var keyStr = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';

    return {
        encode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            do {
                chr1 = input.charCodeAt(i++);
                chr2 = input.charCodeAt(i++);
                chr3 = input.charCodeAt(i++);

                enc1 = chr1 >> 2;
                enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
                enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
                enc4 = chr3 & 63;

                if (isNaN(chr2)) {
                    enc3 = enc4 = 64;
                } else if (isNaN(chr3)) {
                    enc4 = 64;
                }

                output = output +
                    keyStr.charAt(enc1) +
                    keyStr.charAt(enc2) +
                    keyStr.charAt(enc3) +
                    keyStr.charAt(enc4);
                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";
            } while (i < input.length);

            return output;
        },

        decode: function (input) {
            var output = "";
            var chr1, chr2, chr3 = "";
            var enc1, enc2, enc3, enc4 = "";
            var i = 0;

            // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
            var base64test = /[^A-Za-z0-9\+\/\=]/g;
            if (base64test.exec(input)) {
                window.alert("There were invalid base64 characters in the input text.\n" +
                    "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
                    "Expect errors in decoding.");
            }
            input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

            do {
                enc1 = keyStr.indexOf(input.charAt(i++));
                enc2 = keyStr.indexOf(input.charAt(i++));
                enc3 = keyStr.indexOf(input.charAt(i++));
                enc4 = keyStr.indexOf(input.charAt(i++));

                chr1 = (enc1 << 2) | (enc2 >> 4);
                chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
                chr3 = ((enc3 & 3) << 6) | enc4;

                output = output + String.fromCharCode(chr1);

                if (enc3 != 64) {
                    output = output + String.fromCharCode(chr2);
                }
                if (enc4 != 64) {
                    output = output + String.fromCharCode(chr3);
                }

                chr1 = chr2 = chr3 = "";
                enc1 = enc2 = enc3 = enc4 = "";

            } while (i < input.length);

            return output;
        }
    };

});