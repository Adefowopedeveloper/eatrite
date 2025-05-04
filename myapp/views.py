from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, Order, OrderItem
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "home.html")

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
            payment = data.get('payment_method')
            cart = data.get('cart', [])  # [{ name, price, quantity? }]

            if not cart:
                return JsonResponse({'error': 'Cart is empty.'}, status=400)

            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                address=address,
                phone=phone,
                payment_method=payment,
                total_price=0
            )

            total = 0
            for item in cart:
                name = item.get('name')
                price = float(item.get('price', 0))
                quantity = item.get('quantity', 1)

                # In a real system, you'd match name to Product and validate price
                product, created = Product.objects.get_or_create(name=name, defaults={'price': price})
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                total += price * quantity

            order.total_price = total
            order.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)