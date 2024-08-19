import logging
from django.contrib import admin
from .models import Product, Order, CustomUser
from django.contrib.auth.admin import UserAdmin

logger = logging.getLogger(__name__)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

    def save_model(self, request, obj, form, change):
        logger.info(f"Сохранение модели Product: {obj}")
        super().save_model(request, obj, form, change)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at', 'total_price')  # Убедитесь, что эти поля существуют в модели Order
    list_filter = ('status',)
    search_fields = ('user__username', 'status')
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']

    def mark_as_processing(self, request, queryset):
        queryset.update(status='Processing')
    mark_as_processing.short_description = "Отметить как 'В обработке'"

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='Shipped')
    mark_as_shipped.short_description = "Отметить как 'Отправлен'"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
    mark_as_delivered.short_description = "Отметить как 'Доставлен'"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')
    mark_as_cancelled.short_description = "Отметить как 'Отменен'"

# Регистрируем CustomUser только если он используется в проекте
admin.site.register(CustomUser, UserAdmin)






