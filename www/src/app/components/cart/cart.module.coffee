cart = angular.module('cart', [
	'ui.router'
	'services'
])

cart.config(($stateProvider) ->
	$stateProvider
		.state('base.cart', {
			url: '/cart'
			controller: 'cartController'
			templateUrl: 'partials/base.cart.partial.html'
		})
)