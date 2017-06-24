(function(angular) {
  'use strict';
  var myApp = angular.module('myApp', []);

  myApp.controller(
    "TradeController",
    [
      "$scope",
      "$http",
      function($scope, $http) {
        $scope.post = function() {
          var data={
            param1: "hello",
            param2: "next"
          };
          $http.post("/mysite_trade/buy/", data).then(
            function successCallback(response) {
              $scope.result = response.data;
              console.log(response);
            },
            function errorCallback(response) {
              console.log(response);
            }
          );
        };
      }
    ]
  );
})(window.angular);
