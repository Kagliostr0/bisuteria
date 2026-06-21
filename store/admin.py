from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage, Variant


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    fields = ["material", "color", "size", "price_override", "stock", "sku", "image"]
    verbose_name = "Variante"
    verbose_name_plural = "Variantes"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 5
    fields = ["image_preview", "image", "order", "alt_text"]
    readonly_fields = ["image_preview"]
    verbose_name = "Imagen adicional"
    verbose_name_plural = "Imágenes adicionales"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.3);" />', obj.image.url)
        return "—"
    image_preview.short_description = "Vista previa"


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
    inlines = [VariantInline, ProductImageInline]

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
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.3);" />', obj.image.url)
        return "—"
    thumbnail.short_description = "Foto"


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ["variant_thumbnail", "product", "color", "material", "size", "price_override", "stock", "sku"]
    list_filter = ["material", "color"]
    search_fields = ["product__name", "sku"]

    def variant_thumbnail(self, obj):
        img = obj.image or (obj.product.image if obj.product else None)
        if img:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.3);" />', img.url)
        return "—"
    variant_thumbnail.short_description = "Foto"
