from django.contrib import admin

from .models import Category, Product, Variant


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    fields = ["material", "color", "size", "price_override", "stock", "sku", "image"]
    verbose_name = "Variante"
    verbose_name_plural = "Variantes"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "product_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Productos"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["thumbnail", "name", "category", "price", "stock", "available", "created"]
    list_editable = ["price", "stock", "available"]
    list_filter = ["available", "category", "created"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VariantInline]

    fieldsets = [
        ("Información básica", {
            "fields": ["name", "slug", "category"],
            "description": "Datos principales del producto",
        }),
        ("Precio y stock", {
            "fields": ["price", "stock", "available"],
            "description": "Define el precio y la disponibilidad",
        }),
        ("Descripción", {
            "fields": ["description"],
            "description": "Describe tu producto: material, medidas, cuidados",
        }),
        ("Imagen", {
            "fields": ["image"],
            "description": "Sube una foto de alta calidad del producto",
        }),
    ]

    def thumbnail(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover;border-radius:8px;" />'
        return "—"
    thumbnail.short_description = "Foto"
    thumbnail.allow_tags = True


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ["product", "color", "material", "size", "price_override", "stock", "sku"]
    list_filter = ["material", "color"]
    search_fields = ["product__name", "sku"]
