from django.shortcuts import render, reverse
from django.views import View
from .models import *
import datetime
from django.http import JsonResponse
import json
from django.conf import settings
import logging
import ssl
import stripe
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

from .utils import *
# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def shop(request):

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
    stripe_api_key = getattr(settings, 'STRIPE_API_KEY', None)
    if request.method == 'POST':

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': '1000',
                        'product_data': {
                            'name': 'Your Product Name',
                            'images': ['product_image_url'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('paymentComleted')),
            cancel_url=request.build_absolute_uri(reverse('paymentFailed')),
        )

        return JsonResponse({'sessionId': checkout_session.id})
    return render(request, 'pages/checkout.html', cartData(request))

class ProductLandingPageView(TemplateView):
    template_name = "pages/testCheckout.html"
    
@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_RESTRICTED_KEY  # Ensure you're using the SECRET key

        orderTotals = cookieCart(request)
        items = orderTotals['items']

        YOUR_DOMAIN = 'http://127.0.0.1:8000/'
        line_items = []

        for item in items:
            line_items.append({
                'price': item['product']['item_id'],  # Ensure it's a valid Stripe Price ID
                'quantity': item['quantity'],
            })
        
        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=YOUR_DOMAIN + 'paymentCompleted.html',
            cancel_url=YOUR_DOMAIN + 'paymentFailed.html',
            automatic_tax={'enabled': True},
            billing_address_collection='required',
            shipping_address_collection={'allowed_countries': ['US']},
        )
        
        return redirect(checkout_session.url)

def paymentSuccessful(request):
    stripe_api_key = getattr(settings, 'STRIPE_API_KEY', None)
    

logger = logging.getLogger(__name__)

def work(request):
    return render(request, 'pages/work.html')

def about(request):
    return render(request, 'pages/about.html')

def details(request, id):
    product_object = Products.objects.get(id=id)

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

    order = GuestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    return JsonResponse('Transaction has been completed!', safe=False)

def paymentCompletedView(request):
    return render(request, 'pages/paymentCompleted.html')

def paymentFailedView(request):
    return render(request, 'pages/paymentFailed.html')



