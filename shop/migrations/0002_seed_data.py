"""Data-миграция с тестовыми покупателями, товарами и корзинами."""
from decimal import Decimal

from django.db import migrations

CUSTOMERS = [
    ("Иванов Иван", "ivanov@example.com", "+7 900 111-22-33"),
    ("Петрова Анна", "petrova@example.com", "+7 900 222-33-44"),
    ("Сидоров Павел", "sidorov@example.com", ""),
    ("Кузнецова Мария", "kuznetsova@example.com", "+7 900 444-55-66"),
]

PRODUCTS = [
    ("Ноутбук Lenovo IdeaPad 5", "Электроника", "64990.00", True),
    ("Беспроводная мышь", "Электроника", "1490.00", True),
    ("Наушники с шумоподавлением", "Электроника", "12990.00", True),
    ("Кофемашина капсульная", "Бытовая техника", "8990.00", False),
    ("Чайник электрический", "Бытовая техника", "2490.00", True),
    ("Рюкзак городской", "Аксессуары", "3990.00", True),
    ("Термокружка", "Аксессуары", "990.00", True),
    ("Книга «Чистый код»", "Книги", "1290.00", True),
]

# (email покупателя, статус, индексы товаров)
CARTS = [
    ("ivanov@example.com", "paid", [0, 1, 7]),
    ("ivanov@example.com", "active", [6]),
    ("petrova@example.com", "ordered", [2, 5, 6]),
    ("sidorov@example.com", "cancelled", [3]),
    ("kuznetsova@example.com", "active", [4, 6, 7, 1]),
    ("petrova@example.com", "active", []),
]


def seed(apps, schema_editor):
    Customer = apps.get_model("shop", "Customer")
    Product = apps.get_model("shop", "Product")
    Cart = apps.get_model("shop", "Cart")

    customers = {
        email: Customer.objects.create(name=name, email=email, phone=phone)
        for name, email, phone in CUSTOMERS
    }
    products = [
        Product.objects.create(name=n, category=c, price=Decimal(p), in_stock=s)
        for n, c, p, s in PRODUCTS
    ]
    for email, status, idx in CARTS:
        cart = Cart.objects.create(customer=customers[email], status=status)
        cart.products.set([products[i] for i in idx])


def unseed(apps, schema_editor):
    for model in ("Cart", "Product", "Customer"):
        apps.get_model("shop", model).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("shop", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
