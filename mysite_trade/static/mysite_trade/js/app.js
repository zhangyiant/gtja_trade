(function(angular) {
  'use strict';
  var myApp = angular.module('myApp', []);

  myApp.controller(
    "TradeController",
    [
      "$scope",
      "$http",
      function($scope, $http) {
        $scope.symbol = "";
        $scope.price = "0.0";
        $scope.quantity = "0";
        $scope.buy = function() {
          var data={
            symbol: $scope.symbol,
            price: parseFloat($scope.price),
            quantity: parseInt($scope.quantity)
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
        $scope.sell = function() {
          var data={
            symbol: $scope.symbol,
            price: parseFloat($scope.price),
            quantity: parseInt($scope.quantity)
          };
          $http.post("/mysite_trade/sell/", data).then(
            function successCallback(response) {
              $scope.result = response.data;
              console.log(response);
            },
            function errorCallback(response) {
              console.log(response);
            }
          );
        };
        function getStockInfos() {
          $http.get("/mysite_trade/stock_infos/").then(
            function successCallback(response) {
              $scope.stockInfos = response.data.results;
            },
            function errorCallback(response) {
            }
          );
        };
        getStockInfos();
      }
    ]
  );
})(window.angular);
