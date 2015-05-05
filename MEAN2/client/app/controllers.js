angular.module('myApp.controllers', [])

.controller("homeCtrl", function($scope) {
	$scope.people = [];
})


.controller("searchCtrl", function($scope, $http, $routeParams) {
	$http.get('/api/search/' + $routeParams.query).
		success(function(response) {
			$scope.people = response;
		});
})

.controller("profileCtrl", function($scope, $http, $routeParams) {
	$http.get('/api/profile/' + $routeParams.id).
		success(function(response) {
			$scope.person = response;
		});

		console.log(response.jobs);
});