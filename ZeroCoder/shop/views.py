from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib.auth.models import User

# Отображение списка товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

@login_required
def cart(request):
    if request.method == 'POST':
        # Получаем идентификаторы товаров из запроса
        product_ids = request.POST.getlist('product_id')
        products = Product.objects.filter(id__in=product_ids)
        address = request.POST.get('address')

        # Расчет общей суммы заказа
        total_price = sum([product.price for product in products])

        # Создаем заказ
        order = Order.objects.create(user=request.user, delivery_address=address, total_price=total_price)
        order.products.set(products)
        order.save()

        return redirect('order_history')

    products = Product.objects.all()
    return render(request, 'shop/cart.html', {'products': products})

# История заказов пользователя
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})
