'use strict';

var ctfApp = angular.module('ctfApp', [
    'ngRoute',
    'ctfControllers',
    'ngSanitize'
]);

// routing
ctfApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/services', {
        templateUrl: 'static/partials/services.html',
        controller: 'ServicesCtrl'
      }).
      when('/jeopardies', {
        templateUrl: 'static/partials/jeopardies.html',
        controller: 'JeopardiesCtrl'
      }).
      when('/submit_flag', {
        templateUrl: 'static/partials/submit_flag.html',
        controller: 'FlagCtrl'
      }).
      when('/scoreboard', {
        templateUrl: 'static/partials/scoreboard.html',
        controller: 'ScoreboardCtrl'
      }).
      when('/welcome', {
        templateUrl: 'static/partials/welcome.html',
        controller: 'ConfigCtrl'
      }).
      when('/liveshow', {
        templateUrl: 'static/partials/liveshow.html',
        controller: 'LiveshowCtrl'
      }).
      otherwise({
        redirectTo: '/welcome'
      });
  }]);
