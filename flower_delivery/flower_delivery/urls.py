from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('orders.urls')),  # Подключение всех маршрутов из приложения orders
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),  # Перенаправление на каталог
    ]
if settings.DEBUG:  # Добавляем обработку медиафайлов только в режиме разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




