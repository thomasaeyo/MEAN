angular.module("myApp.router", ['ngRoute', 'myApp.controllers'])

.config(function($routeProvider, $locationProvider) {
    $locationProvider.hashPrefix('!');
    $routeProvider.
      when("/", 
      	{ 
      		templateUrl: "/../partials/home.html",
      		controller: "homeCtrl",
      	}).
      when("/search/:query", 
      	{
      		templateUrl: "/../partials/home.html",
      		controller: "searchCtrl",
      	}).
      when("/profile/:id", 
      	{
      		templateUrl: "/../partials/profile.html",
      		controller: "profileCtrl",
      	}).
      otherwise( { redirectTo: "/" });
      $locationProvider.html5Mode(true);
});