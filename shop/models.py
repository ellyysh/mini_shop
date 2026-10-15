from django.db import models


class Customer(models.Model):
    name = models.CharField("ФИО", max_length=150)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    registered_at = models.DateTimeField("Дата регистрации", auto_now_add=True)

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=200)
    category = models.CharField("Категория", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    in_stock = models.BooleanField("В наличии", default=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.price} ₽)"


class Cart(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        ORDERED = "ordered", "Оформлена"
        PAID = "paid", "Оплачена"
        CANCELLED = "cancelled", "Отменена"

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="carts", verbose_name="Покупатель"
    )
    products = models.ManyToManyField(
        Product, related_name="carts", blank=True, verbose_name="Товары"
    )
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Корзина №{self.pk} — {self.customer}"

    @property
    def total_price(self):
        return sum((p.price for p in self.products.all()), 0)
