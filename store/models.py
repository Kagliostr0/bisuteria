from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products",
        verbose_name="Categoría",
    )
    name = models.CharField(max_length=200, verbose_name="Nombre del producto")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True,
        verbose_name="Foto principal",
        help_text="Sube la foto del producto. Se recomienda 600x600 px.",
    )
    description = models.TextField(
        blank=True, verbose_name="Descripción",
        help_text="Describe los detalles: material, medidas, cuidados.",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio ($)",
        help_text="Precio base del producto.",
    )
    stock = models.PositiveIntegerField(
        default=0, verbose_name="Stock",
        help_text="Cantidad disponible en inventario.",
    )
    available = models.BooleanField(
        default=True, verbose_name="Disponible",
        help_text="Desmarca si el producto no está a la venta.",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug, self.slug])


class Variant(models.Model):
    MATERIAL_CHOICES = [
        ("oro_18k", "Oro 18K"),
        ("oro_rosa", "Oro Rosa"),
        ("plata", "Plata"),
        ("acero", "Acero Quirúrgico"),
    ]
    COLOR_CHOICES = [
        ("dorado", "Dorado"),
        ("plateado", "Plateado"),
        ("rosado", "Rosado"),
        ("negro", "Negro"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants",
        verbose_name="Producto",
    )
    material = models.CharField(
        max_length=50, choices=MATERIAL_CHOICES, default="oro_18k",
        verbose_name="Material",
    )
    color = models.CharField(
        max_length=50, choices=COLOR_CHOICES, default="dorado",
        verbose_name="Color",
    )
    size = models.CharField(
        max_length=50, blank=True, verbose_name="Talla/Medida",
        help_text="Ej: 7 (anillo), 45 cm (collar), Única",
    )
    price_override = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True,
        verbose_name="Precio especial ($)",
        help_text="Si está vacío, usa el precio del producto.",
    )
    stock = models.PositiveIntegerField(
        default=0, verbose_name="Stock de esta variante",
    )
    image = models.ImageField(
        upload_to="variants/", blank=True, null=True,
        verbose_name="Foto de la variante",
        help_text="Opcional. Si no se sube, se usa la foto del producto.",
    )
    sku = models.CharField(
        max_length=100, blank=True, unique=True, verbose_name="SKU/Código",
        help_text="Código interno del producto.",
    )

    class Meta:
        verbose_name = "Variante"
        verbose_name_plural = "Variantes"
        unique_together = ["product", "material", "color", "size"]

    def __str__(self):
        return f"{self.product.name} - {self.get_color_display()} / {self.get_material_display()}"
