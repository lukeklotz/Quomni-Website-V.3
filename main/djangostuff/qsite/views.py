from django.shortcuts import render
from .models import *
import datetime
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.conf import settings
import logging
import ssl

from .utils import *
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def shop(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Products.objects.all()
    context = {'products':products, 'cartItems': cartItems}

    return render(request, 'pages/shop.html', context)

def cart(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    if isEmpty(cartItems) == 1:
        return render(request, 'pages/cartEmpty.html', cartData(request))
    else:
        return render(request, 'pages/cart.html', cartData(request))

def checkout(request):
    return render(request, 'pages/checkout.html', cartData(request))



logger = logging.getLogger(__name__)

def send_email(request):

    try:
        cart_data = cookieCart(request)

        items = cart_data['items']
        order = cart_data['order']
        cart_items_count = cart_data['cartItems']

        # Accumulate product names in a string
        product_names = ""
        for item in items:
            product_name = item['product']['name']
            product_names += f"{product_name}\n"

        subject = 'Someone purchased items from your shop!'
        from_email = 'lukeklotz@outlook.com'
        recipient = ['lukeklotz@gmail.com']

        send_mail(
            subject,
            product_names,
            from_email,
            recipient,
        )

        # Log success message
        logger.info("Email sent successfully!")
    except Exception as e:
        # Log error message
        logger.error(f"Error sending email: {str(e)}")

    return render(request, 'pages/index.html', cartData(request))



def work(request):
    return render(request, 'pages/work.html')

def about(request):
    return render(request, 'pages/about.html')

def details(request, id):
    product_object = Products.objects.get(id=id)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']

    products = Products.objects.all()
    context = {'products':products, 'cartItems': cartItems, 'product_object':product_object}


    return render(request, 'pages/details.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        total = float(data['from']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
    else:
        order = GuestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse('Transaction has been completed!', safe=False)