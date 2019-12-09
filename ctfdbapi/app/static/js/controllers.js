'use strict';

var ctfControllers = angular.module('ctfControllers', []);

ctfControllers.controller('ServicesCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $http.get('/services').success(function(data) {
          $scope.services = data;
      });
      $http.get('/services_status').success(function(data) {
          $scope.services_status = data;
      });
  }]);


ctfControllers.controller('JeopardiesCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $http.get('/jeopardies').success(function(data) {
          $scope.jeopardies = data;
      });
  }]);


ctfControllers.controller('FlagCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $scope.flag = '';
      $scope.result = '';

      $scope.submit = function() {
          if ($scope.flag) {
            $http.post('/flag', {'flag': $scope.flag}).success(function(data) {
                $scope.result = data;
            })
          }
      }
  }]);

ctfControllers.controller('ScoreboardCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $http.get('/scores').success(function(data) {
          $scope.scores = Object.keys(data).map(function(key) {
              return {"team_name" : key, "score" : data[key] }
            });
      });
  }]);

ctfControllers.controller('ToggleCtrl', ['$scope',
  function ($scope) {
      $scope.visible = false;

      $scope.toggle = function() {
          $scope.visible = !$scope.visible;
      };
  }]);

ctfControllers.controller('ConfigCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $http.get('/config').success(function(data) {
          $scope.config = data;
      });
  }]);

// Controller for the lifeshow
// ctfControllers is the var from above
// http get is to get Data from the DB
ctfControllers.controller('LiveshowCtrl', ['$scope', '$http',
  function ($scope, $http) {
      $scope.pc = "pc.png"; // possible that the whole path is there, in the teamplate ypu need ng-src
      $scope.arrow = "arrow.png";
      // need Inforamtion from Table Submission --> attending_team and flag_id
      // need Information from Talbe Flag --> same flag_id and attending_team
      $http.get('/reasons').success(function(response) { // here i need the path to my sql

        // Object returns an array with given objects
        // map retruns you the value instead of the key
        $scope.grund = response.data;
      });
  }]);

  // wo steht unsere Verbindung zu unserer Datenbank
  // data gibt dir die get anfrage zurück mit den daten, status, config, method
  // https://www.w3schools.com/angular/tryit.asp?filename=try_ng_http_get
  // data is carrying the response from the server
  

