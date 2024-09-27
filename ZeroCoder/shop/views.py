from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponse

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


@login_required
def cart(request):
    if request.method == 'POST':
        # Получаем товары из корзины
        product_ids = request.POST.getlist('product_ids')
        products = Product.objects.filter(id__in=product_ids)
        address = request.POST.get('address')

        # Создаем заказ
        order = Order.objects.create(user=request.user, delivery_address=address)
        order.products.set(products)
        order.save()
        return redirect('order_history')

    products = Product.objects.all()
    return render(request, 'shop/cart.html', {'products': products})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})
