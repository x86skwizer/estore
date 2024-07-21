from django.shortcuts import render, get_object_or_404
from .cart import Cart
from core.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def cart_summary(request):
     # Get the cart
     cart = Cart(request)
     cart_products = cart.get_prods
     quantities = cart.get_quants
     totals = cart.cart_total
     return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals":totals})

def cart_add(request):
    cart = Cart(request)
    
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')
        
        print("Received POST data:", request.POST)  # Debugging line

        if product_id and product_qty:
            try:
                product_id = int(product_id)
                product_qty = int(product_qty)
                product = get_object_or_404(Product, id=product_id)
                cart.add(product=product, quantity=product_qty)
                cart_quantity = cart.__len__()
                messages.success(request, ("Item added to cart successfully !"))
                return JsonResponse({'message': 'Product added to cart successfully.', 'qty': cart_quantity})
            
            except (ValueError, Product.DoesNotExist):
                return JsonResponse({'error': 'Invalid product ID or product does not exist.'}, status=400)
        else:
            return JsonResponse({'error': 'Product ID is missing.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method or action.'}, status=405)

def cart_delete(request):
    cart = Cart(request)

    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        if product_id:
            try:
                product_id = int(product_id)
                product = get_object_or_404(Product, id=product_id)
                cart.remove(product)
                messages.success(request, ("Item deleted !"))
                return JsonResponse({'message': 'Product removed from cart successfully.', 'product_name': product.name})

            except ValueError:
                return JsonResponse({'error': 'Invalid product ID.'}, status=400)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist.'}, status=400)
        else:
            return JsonResponse({'error': 'Product ID is missing.'}, status=400)

    return JsonResponse({'error': 'Invalid request method or action.'}, status=405)

def cart_update(request):
    cart = Cart(request)
    
    if request.method == 'POST' and request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = request.POST.get('product_qty')

        print("Received POST data:", request.POST)  # Debugging line

        if product_id and product_qty:
            try:
                product_id = int(product_id)
                product_qty = int(product_qty)
                
                product = get_object_or_404(Product, id=product_id)
                cart.update(product=product, quantity=product_qty)
                messages.success(request, ("Cart updated !"))
                return JsonResponse({'message': 'Product updated in cart successfully.', 'product_name': product.name})
            
            except ValueError:
                return JsonResponse({'error': 'Invalid product ID or quantity.'}, status=400)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product does not exist.'}, status=400)
        else:
            return JsonResponse({'error': 'Product ID or quantity is missing.'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method or action.'}, status=405)
