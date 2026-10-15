from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from shop import views

admin.site.site_header = "Магазин — администрирование"
admin.site.index_title = "Управление магазином"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("carts/", views.cart_list, name="cart_list"),
    path("", RedirectView.as_view(pattern_name="cart_list")),
]
