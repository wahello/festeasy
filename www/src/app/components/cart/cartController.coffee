cart.controller('cartController', (
		$scope,
		authService,
		$auth,
		$state,
		userService,
		cartProductService,
		festivalService,
		ngNotify,
		cartService) ->
	
	authenticatedUser = authService.getAuthenticatedUser()

	cart = userService.one(authenticatedUser.id).one('cart')

	$scope.updateSelectedFestival = (festival, model) ->
		patchCart = cart.patch({festival_id: festival.id})
		patchCart.then((response) ->
			updateCart()
		)

	updateCart = () ->
		festivalStart = moment().add(7, 'days').format()
		getCart = cart.get()
		getCart.then((response) ->
			$scope.cart = response
			getFestivals = festivalService.getList({'starts-on-gt': festivalStart})
			getFestivals.then((response) ->
				$scope.festivals = response
				if $scope.cart.festival_id
					for festival in $scope.festivals
						if $scope.cart.festival_id == festival.id
							$scope.selectedFestival = festival
			)
		)

		getCart.catch((response) ->
			$scope.error = true
		)

		getCartProducts = cart.all('cart-products').getList()
		getCartProducts.then((response) ->
			$scope.cartProducts = response
		)

	$scope.remove = (cartProduct) ->
		removeCartProduct = cartProductService.one(cartProduct.id).remove()
		removeCartProduct.then((response) ->
			updateCart()
		)

	$scope.checkout = () ->
		if not $scope.cartProducts.length
			ngNotify.set('Please add at least one item to your cart.', 'error')
			return
		if not $scope.cart.festival_id
			ngNotify.set('Please select a festival.', 'error')
			return
		$state.go('base.checkout')

	updateCart()
)