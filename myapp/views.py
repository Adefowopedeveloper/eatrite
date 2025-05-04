import random
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Order, OrderItem


def home(request):
    all_products = list(Product.objects.exclude(image=''))  # Only products with images
    random.shuffle(all_products)
    selected_products = all_products[:20]  # Select random 20
    return render(request, "home.html", {'carousel_images': selected_products})


def menu(request):
    foods = Product.objects.filter(category__name='Foods')
    drinks = Product.objects.filter(category__name='Drinks')
    cakes = Product.objects.filter(category__name='Cakes')
    return render(request, 'menu.html', {
        'foods': foods,
        'drinks': drinks,
        'cakes': cakes
    })


def cart(request):
    return render(request, "cart.html")


def about(request):
    return render(request, "about.html")


@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            address = data.get('address')
            phone = data.get('phone')
            note = data.get('note', '')
            payment_method = data.get('payment_method')
            cart = data.get('cart', [])

            if not cart:
                return JsonResponse({'error': 'Cart is empty.'}, status=400)

            # Create Order record
            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                address=address,
                phone=phone,
                note=note,
                payment_method=payment_method,
                total_price=0  # Will be updated after calculating total
            )

            total = 0
            for item in cart:
                product_name = item.get('name')
                price = float(item.get('price', 0))
                quantity = item.get('quantity', 1)

                # Fetch product by name (or return error if not found)
                try:
                    product = Product.objects.get(name=product_name)
                except Product.DoesNotExist:
                    return JsonResponse({'error': f'Product "{product_name}" not found.'}, status=404)

                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                total += price * quantity

            order.total_price = total
            order.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)
