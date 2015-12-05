festivals.controller('festivalsController', ($scope, $state, festivalService, authService, userService) ->
	getFestivals = festivalService.getList()
	getFestivals.then((response) ->
		$scope.festivals = response
	)
	getFestivals.catch((response) ->
		$scope.error = true
	)
	
	$scope.selectFestival = (festival) ->
		authenticatedUser = authService.getAuthenticatedUser()
		if authenticatedUser
			cart = userService.one(authenticatedUser.id).one('cart')
			patchCart = cart.patch({festival_id: festival.id})
			patchCart.then((response) ->
				$state.go('base.store.products')
			)
		else
			currentUrl = $state.href('base.signin', {}, {absolute: true})
			$state.go('base.signin', {
				returnStateName: 'base.festivals',
				redirectReason: 'Auth needed.',
				message: 'Please sign in to select a festival.'
			})
)
