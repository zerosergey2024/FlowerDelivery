# flowers/views.py

from django.shortcuts import render
from .models import Product, Order, Review

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'shop/order_list.html', {'orders': orders})

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'shop/review_list.html', {'reviews': reviews})