from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
# Create your views here.

def store(request):    #function base view
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # order is parent and orderitem is child
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request,'store/store.html',context)


def cart(request):

    if request.user.is_authenticated:
        customer= request.user.customer
        order, created =Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()#order is parent and orderitem is child
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()  # order is parent and orderitem is child
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']
    print('productId:',productId)
    print('action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('item was added', safe=False)

def processOrder(request):
    print("ali")
    print('Data:',request.body)
    return JsonResponse('Payment Complete!',safe=False)
