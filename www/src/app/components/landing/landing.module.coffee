landing = angular.module('landing', [
	'ui.router',
])

landing.config(($stateProvider) ->
    $stateProvider
        .state('base.landing', {
            url: '/'
            templateUrl: 'landing.partial.html'
        })
)
