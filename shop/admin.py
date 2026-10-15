from django.contrib import admin
from django.db.models import Count, Sum

from .models import Cart, Customer, Product


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "carts_count", "registered_at")
    list_filter = ("registered_at",)
    search_fields = ("name", "email", "phone")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_carts_count=Count("carts"))

    @admin.display(description="Корзин", ordering="_carts_count")
    def carts_count(self, obj):
        return obj._carts_count


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock")
    list_filter = ("category", "in_stock")
    list_editable = ("price", "in_stock")
    search_fields = ("name", "category")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "products_count", "total", "created_at")
    list_display_links = ("id", "customer")
    list_filter = ("status", "created_at", "customer")
    search_fields = ("customer__name", "customer__email", "products__name")
    filter_horizontal = ("products",)
    date_hierarchy = "created_at"
    list_select_related = ("customer",)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _products_count=Count("products", distinct=True),
            _total=Sum("products__price"),
        )

    @admin.display(description="Кол-во товаров", ordering="_products_count")
    def products_count(self, obj):
        return obj._products_count

    @admin.display(description="Сумма, ₽", ordering="_total")
    def total(self, obj):
        return obj._total or 0
