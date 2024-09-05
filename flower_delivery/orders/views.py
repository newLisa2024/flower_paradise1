from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Order, Cart, CartItem, OrderItem
from .forms import RegistrationForm, CheckoutForm, ProductForm, OrderForm
from rest_framework import viewsets
from .serializers import ProductSerializer, OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'orders/registration.html', {'form': form})

def home(request):
    return render(request, 'orders/home.html')
def catalog(request):
    products = Product.objects.all()
    return render(request, 'orders/catalog.html', {'products': products})
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Добавляем атрибут queryset
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Возвращаем заказы, связанные с текущим пользователем
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def user_orders(self, request):
        # Возвращаем заказы текущего пользователя
        orders = self.get_queryset()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('checkout')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, OrderItem, Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user, active=True)
    except Cart.DoesNotExist:
        # Если активной корзины нет, создайте новую или перенаправьте на другую страницу
        return redirect('catalog')  # Например, перенаправление в каталог для выбора товаров
    items_in_cart = cart.cartitem_set.all()
    total_price = sum(item.get_total_price() for item in items_in_cart)
    return render(request, 'orders/checkout.html', {'items_in_cart': items_in_cart, 'total_price': total_price})

@login_required
def order_checkout(request):
    cart = get_object_or_404(Cart, user=request.user, active=True)
    items_in_cart = cart.cartitem_set.all()
    total_price = sum(item.get_total_price() for item in items_in_cart)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.payment_method = form.cleaned_data['payment_method']
            order.delivery_address = form.cleaned_data['delivery_address']
            order.status = 'В обработке'  # Убедитесь, что статус задан
            order.save()
            for item in items_in_cart:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.active = False
            cart.save()
            return redirect('order_history')
    else:
        form = OrderForm()
    # Важно: этот return должен быть вне блока if-else, чтобы его всегда выполняли
    return render(request, 'orders/order_checkout.html', {
        'form': form,
        'items_in_cart': items_in_cart,
        'total_price': total_price})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Убедитесь, что заказы фильтруются по пользователю
    return render(request, 'orders/order_history.html', {'orders': orders})

@staff_member_required
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'orders/admin_dashboard.html', {'products': products})

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm()
    return render(request, 'orders/add_product.html', {'form': form})

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'orders/edit_product.html', {'form': form})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_dashboard')