import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    print('cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            
            product = Products.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product':{
                    'item_id': product.item_id, # used for stripe payment
                    'id': product.id,
                    'name': product.title,
                    'price': product.price,
                    'image': product.image,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            print("Adding item_id:", product.item_id)  # Add this line to check item_id
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order, 'cartItems':cartItems}

def cartData(request):

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
            order = cookieData['order']
            items = cookieData['items']

        return {'items':items, 'order':order, 'cartItems':cartItems}

def isEmpty(cartItems):
    if not cartItems:
      print('cart is empty')
      return 1 
    else:
      print('cart is not empty')
      return 0
    
def GuestOrder(request, data):
    print('User is not logged in')
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    
    order = Order.objects.create(
        complete=False,
    )

    for item in items:
        product = Products.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return order