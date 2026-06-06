from django.db import models

from store.models import Product, Variant


class Order(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo electrónico")
    address = models.CharField(max_length=250, verbose_name="Dirección")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Estado")
    zip_code = models.CharField(max_length=20, verbose_name="Código postal")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    paid = models.BooleanField(default=False, verbose_name="Pagado")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    variant = models.ForeignKey(
        Variant, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="order_items", verbose_name="Variante",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Artículo del pedido"
        verbose_name_plural = "Artículos del pedido"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
