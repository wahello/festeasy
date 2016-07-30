module.exports = [
  {
    name: 'cart',
    endpoint: 'carts',
    relations: {
      hasMany: {
        cartProduct: {
          localField: 'cart_products',
          foreignKey: 'cart_id',
        },
      },
    },
  },
  {
    name: 'cartProduct',
    endpoint: 'cart-products',
    relations: {
      belongsTo: {
        cart: {
          localField: 'cart',
          localKey: 'cart_id',
        },
      },
    },
  },
  {
    name: 'product',
    endpoint: 'products',
  },
  {
    name: 'payu-transaction',
    endpoint: 'payu-transactions',
  },
  {
    name: 'festival',
    endpoint: 'festivals',
  },
  {
    name: 'order',
    endpoint: 'orders',
  },
  {
    name: 'user',
    endpoint: 'users',
  },
]