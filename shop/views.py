from django.db.models import Q
from django.shortcuts import render

from .models import Cart


def cart_list(request):
    carts = Cart.objects.select_related("customer").prefetch_related("products")

    status = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()
    if status:
        carts = carts.filter(status=status)
    if query:
        carts = carts.filter(
            Q(customer__name__icontains=query)
            | Q(customer__email__icontains=query)
            | Q(products__name__icontains=query)
        ).distinct()

    return render(request, "shop/cart_list.html", {
        "carts": carts,
        "statuses": Cart.Status.choices,
        "current_status": status,
        "query": query,
    })
