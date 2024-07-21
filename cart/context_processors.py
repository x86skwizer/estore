from .cart import Cart


# Creat context processor to cart to work on all site
def cart(request):
	# Return the default data from cart
	return {'cart': Cart(request)}