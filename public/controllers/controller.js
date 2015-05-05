var myApp = angular.module('myApp',[]);

myApp.controller('AppCtrl', ['$scope', '$http', function($scope, $http) {
	console.log("Hello from controller");
	$scope.people = [];	

	$scope.search = function() {
		console.log($scope.query);
		$http.post('/search', {query:$scope.query}).success(function(response) {
			console.log(response);
			$scope.people = response;
		});
	};
}]);