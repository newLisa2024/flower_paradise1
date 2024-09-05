from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='orders/logout.html'), name='logout'),
    path('catalog/', views.catalog, name='catalog'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_checkout/', views.order_checkout, name='order_checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('api/', include(router.urls)),  # Added the API routes here
    path('api/orders/user/', OrderViewSet.as_view({'get': 'user_orders'})),  # Добавляем путь для получения заказов
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






