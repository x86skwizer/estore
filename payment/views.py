from django.shortcuts import render, redirect
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from cart.cart import Cart
from django.contrib import messages
from core.models import Product, Profile
import datetime


def payment_success(request):
	return render(request, "payment/payment_success.html", {})


def checkout(request):
	cart = Cart(request) # Get the cart
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	if request.user.is_authenticated:
		# Checkout as logged in user
		shipping_user = ShippingAddress.objects.get(user__id=request.user.id) # Shipping User
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user) # Shipping Form
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		shipping_form = ShippingForm(request.POST or None) # Checkout as guest
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def billing_info(request):
	if request.POST:
		cart = Cart(request) # Get the cart
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()
		my_shipping = request.POST # Create a session with Shipping Info
		request.session['my_shipping'] = my_shipping
		if request.user.is_authenticated: # Check to see if user is logged in
			billing_form = PaymentForm() # Get The Billing Form
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
		else: # Not logged in
			billing_form = PaymentForm() # Get The Billing Form
			return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
	else:
		messages.success(request, "Access Denied")
		return redirect('core:index')


def process_order(request):
	if request.POST:
		cart = Cart(request) # Get the cart
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()
		payment_form = PaymentForm(request.POST or None) # Get Billing Info from the last page
		my_shipping = request.session.get('my_shipping') # Get Shipping Session Data
		full_name = my_shipping['shipping_full_name'] # Gather Order Info
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals
		if request.user.is_authenticated: # Create an Order
			user = request.user # logged in
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid) # Create Order
			create_order.save()
			# Add order items
			order_id = create_order.pk # Get the order ID
			for product in cart_products(): # Get product Info
				product_id = product.id # Get product ID
				price = product.price # Get product price
				for key,value in quantities().items(): # Get quantity
					if int(key) == product.id:
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price) # Create order item
						create_order_item.save()
			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key] # Delete the key
			current_user = Profile.objects.filter(user__id=request.user.id) # Delete Cart from Database (old_cart field)
			current_user.update(old_cart="") # Delete shopping cart in database (old_cart field)
			messages.success(request, "Order Placed !")
			return redirect('core:index')
		else: # not logged in
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid) # Create Order
			create_order.save()
			# Add order items
			order_id = create_order.pk # Get the order ID
			for product in cart_products(): # Get product Info
				product_id = product.id # Get product ID
				if product.is_sale: # Get product price
					price = product.sale_price
				else:
					price = product.price
				for key,value in quantities().items(): # Get quantity
					if int(key) == product.id:
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price) # Create order item
						create_order_item.save()
			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					del request.session[key] # Delete the key
			current_user = Profile.objects.filter(user__id=request.user.id) # Delete Cart from Database (old_cart field)
			current_user.update(old_cart="") # Delete shopping cart in database (old_cart field)
			messages.success(request, "Order Placed !")
			return redirect('core:index')
	else:
		messages.success(request, "Access Denied !")
		return redirect('core:index')


def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num) # Grab the order
			now = datetime.datetime.now() # Grab date and time
			order.update(shipped=True, date_shipped=now) # Update order
			messages.success(request, "Shipping Status Updated")
			return redirect('core:index')
		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('core:index')


def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			order = Order.objects.filter(id=num) # Grab the order
			now = datetime.datetime.now() # Grab date and time
			order.update(shipped=False, date_shipped=now) # Update order
			messages.success(request, "Shipping Status Updated")
			return redirect('core:index')
		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('core:index')
	

def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		order = Order.objects.get(id=pk) # Get the order
		items = OrderItem.objects.filter(order=pk) # Get the order items
		if request.POST:
			status = request.POST['shipping_status']
			if status == "true":
				order = Order.objects.filter(id=pk) # Get the order
				now = datetime.datetime.now() # Update shipping date
				order.update(shipped=True, date_shipped=now) # Update the status
			else:
				order = Order.objects.filter(id=pk) # Get the order
				order.update(shipped=False) # Update the status
			messages.success(request, "Shipping Status Updated")
			return redirect('core:index')
		return render(request, 'payment/orders.html', {"order":order, "items":items})
	else:
		messages.success(request, "Access Denied")
		return redirect('core:index')