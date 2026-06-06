from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "price", "quantity"]


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
