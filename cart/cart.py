from core.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # Get the current session cart if it exists, otherwise create a new one
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        # Make sure cart is available on all site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            pass
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'': ,} to {"": ,}
            cart = str(self.cart)
            carty = cart.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        ret_var = self.cart
        return ret_var

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {'quantity': quantity, 'price': str(product.price)}
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'': ,} to {"": ,}
            cart = str(self.cart)
            carty = cart.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        ret_var = self.cart
        return ret_var

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        total = 0
        for product in products:
            total += product.price * self.cart[str(product.id)]['quantity']
        return total


    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        # Return those look up products
        return products
    
    def get_quants(self):
        quantities = {product_id: item['quantity'] for product_id, item in self.cart.items()}
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product.id)
        # Update cart(Dictionnary)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.session.modified = True
        ret_var = self.cart
        return ret_var
    
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'': ,} to {"": ,}
            cart = str(self.cart)
            carty = cart.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        ret_var = self.cart
        return ret_var
