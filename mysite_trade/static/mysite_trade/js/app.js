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
              $scope.stockInfos = [];
              $scope.nobleMetalInfos = [];
              var results = response.data.results;
              var counter;
              for (counter = 0; counter < results.length; counter++) {
                var symbol = results[counter].symbol;
                var t = symbol.charAt(0);
                if (t <= "9" && t >= "0") {
                  $scope.stockInfos.push(results[counter]);
                } else {
                  $scope.nobleMetalInfos.push(results[counter]);
                }
              }
            },
            function errorCallback(response) {
            }
          );
        };
        $scope.nobleMetalSymbol = "";
        $scope.nobleMetalPrice = "0.0";
        $scope.nobleMetalQuantity = "0";
        $scope.nobleMetalBuy = function() {
          var data={
            symbol: $scope.nobleMetalSymbol,
            price: parseFloat($scope.nobleMetalPrice),
            quantity: parseInt($scope.nobleMetalQuantity)
          };
          $http.post("/mysite_trade/noble-metal-buy/", data).then(
            function successCallback(response) {
              $scope.nobleMetalResult = response.data;
              console.log(response);
            },
            function errorCallback(response) {
              console.log(response);
            }
          );
        };
        $scope.nobleMetalSell = function() {
          var data={
            symbol: $scope.nobleMetalSymbol,
            price: parseFloat($scope.nobleMetalPrice),
            quantity: parseInt($scope.nobleMetalQuantity)
          };
          $http.post("/mysite_trade/noble-metal-sell/", data).then(
            function successCallback(response) {
              $scope.nobleMetalResult = response.data;
              console.log(response);
            },
            function errorCallback(response) {
              console.log(response);
            }
          );
        };
        getStockInfos();
      }
    ]
  );
})(window.angular);
