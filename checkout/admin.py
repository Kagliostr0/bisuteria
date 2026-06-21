from django.contrib import admin
from django.utils.html import format_html

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["order_thumbnail", "product", "variant", "price", "quantity"]

    def order_thumbnail(self, obj):
        if obj.variant and obj.variant.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:6px;" />', obj.variant.image.url)
        if obj.product and obj.product.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:6px;" />', obj.product.image.url)
        return "—"
    order_thumbnail.short_description = "Foto"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "full_name", "email", "total", "paid", "created"]
    list_filter = ["paid", "created"]
    search_fields = ["first_name", "last_name", "email"]
    readonly_fields = ["created", "updated"]
    inlines = [OrderItemInline]

    fieldsets = [
        ("Cliente", {
            "fields": ["first_name", "last_name", "email", "phone"],
        }),
        ("Dirección de envío", {
            "fields": ["address", "city", "state", "zip_code"],
        }),
        ("Pago", {
            "fields": ["paid"],
        }),
    ]

    def order_id(self, obj):
        return f"#{obj.id}"
    order_id.short_description = "Pedido"

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Cliente"

    def total(self, obj):
        return f"${obj.get_total_cost()}"
    total.short_description = "Total"
