angular.module('myApp.controllers', [])

.controller("homeCtrl", function($scope) {
	$scope.people = [];
})


.controller("searchCtrl", function($scope, $http, $routeParams) {
	console.log("in searchCtrl");
	$http.get('/api/search/' + $routeParams.query).
		success(function(response) {
			$scope.people = response;
		});
	$scope.quantity = 20;
	$scope.orderProp = "last_name";
})

.controller("profileCtrl", function($scope, $http, $routeParams) {
	$http.get('/api/profile/' + $routeParams.id).
		success(function(response) {
			$scope.person = response;
			// if(person.jobs)
		});
});