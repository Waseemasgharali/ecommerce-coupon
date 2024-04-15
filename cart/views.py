from unicodedata import name
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from numpy import product
from cart.models import Cart, PlaceOrder, Coupon
from products.models import Product, Color, Size
from django.db.models import Q
from account.models import User
from account.forms import EditUserAddressForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
import stripe
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

import json
stripe.api_key = settings.STRIPE_SECRET_KEY

# Function to create a checkout session for Stripe payment
def create_checkout_session(request):
    data = json.loads(request.body)
    total_amount = data['amount']
    total_amount = int(total_amount * 100)
    base_url = request.build_absolute_uri('/')[:-1]  # Remove trailing slash
    success_url = f'{base_url}/cart/paymentdone'
    cancel_url = f'{base_url}/cart/checkout'

    if request.method == 'POST':
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Total Amount',
                    },
                    'unit_amount': total_amount, # in cents, meaning $20.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=request.user.email,
        )
        return JsonResponse({
            'id': session.id
        })
    return redirect('index')

# Function to add a product to the cart
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')

    color = Color.objects.get(id=color_id) if color_id else None
    size = Size.objects.get(id=size_id) if size_id else None

    Cart(user=user, product=product, color=color, size=size).save()
    return redirect('shop_cart')

# Function to display the shopping cart
@login_required
def shop_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user).order_by('-pk')
    total_amount = 0.0
    summary_amount = 0.0
    summary_shipping = 0.0

    for item in cart:
        item_amount = item.quantity * (item.product.selling_price + item.product.shipping_price)
        total_amount += item_amount
        summary_shipping += (item.quantity * item.product.shipping_price)
        summary_amount += (item.quantity * item.product.selling_price)

    return render(request, 'product/cart.html', {'cart': cart, 'totalamount': total_amount, 'summary_shipping': summary_shipping, 'summary_amount': summary_amount})

# Function to increase quantity of a product in the cart
@login_required
def plus_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart_item = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        cart_item.quantity += 1
        cart_item.save()

        return JsonResponse({'quantity': cart_item.quantity})

# Function to decrease quantity of a product in the cart
@login_required
def minus_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart_item = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        return JsonResponse({'quantity': cart_item.quantity})

# Function to remove a product from the cart
@login_required
def remove_cart(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart_item = Cart.objects.get(Q(id=cart_id) & Q(user=request.user))
        cart_item.delete()

        return JsonResponse({'status': 'success'})

# Function to edit user address
@login_required
def editaddress(request):
    if request.method == "POST":
        form = EditUserAddressForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('checkout')
    else:
        form = EditUserAddressForm(instance=request.user)
    return render(request, 'product/addressedit.html', {'form': form})

# Function to display checkout page
@login_required
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user).order_by('-pk')
    total_amount = 0.0
    summary_amount = 0.0
    summary_shipping = 0.0

    for item in cart_items:
        item_amount = item.quantity * (item.product.selling_price + item.product.shipping_price)
        total_amount += item_amount
        summary_shipping += (item.quantity * item.product.shipping_price)
        summary_amount += (item.quantity * item.product.selling_price)

    # Fetch available coupons for the user
    coupons = Coupon.objects.filter(active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())

    return render(request, 'product/checkout.html', {'cart_items': cart_items, 'total_amount': total_amount, 'summary_amount': summary_amount, 'summary_shipping': summary_shipping, 'coupons': coupons})

# Function to process payment
@login_required
def payment_done(request):
    user = request.user
    name = user.first_name + user.last_name
    address = user.address
    state = user.state
    city = user.city
    zip_code = user.zip_code
    phone = user.phone
    cart_items = Cart.objects.filter(user=user)

    for cart_item in cart_items:
        if cart_item.color:
            color = cart_item.color.name
        else:
            color = "None"

        if cart_item.size:
            size = cart_item.size.name
        else:
            size = "None"
        
        order_price = cart_item.quantity * (cart_item.product.selling_price + cart_item.product.shipping_price)
        PlaceOrder(user=user, name=name, address=address, state=state, city=city, phone=phone, zip_code=zip_code, quantity=cart_item.quantity, product=cart_item.product, color=color, order_price=order_price, size=size).save()
        cart_item.delete()

    return redirect('order')

# Function to display orders
@login_required
def order(request):
    user = request.user
    orders = PlaceOrder.objects.filter(user=user).order_by('-pk')
    return render(request, 'product/order.html', {'orders': orders})

@require_POST
@login_required
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        cart_items = Cart.objects.filter(user=request.user)
        
        total_amount = sum(Decimal(item.product.selling_price) * item.quantity for item in cart_items)
        print("Total Amount Before Discount:", total_amount)  # Debug print
        
        discount_amount = total_amount * (coupon.discount_percentage / Decimal(100))
        print("Discount Amount:", discount_amount)  # Debug print
        
        discounted_total_amount = total_amount - discount_amount
        print("Discounted Total Amount:", discounted_total_amount)  # Debug print
        
        # Update the total amount based on the coupon application
        return JsonResponse({'success': True, 'message': 'Coupon applied successfully!', 'total_amount': discounted_total_amount})
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code or coupon expired.'})
