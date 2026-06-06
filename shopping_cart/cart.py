from decimal import Decimal

from django.conf import settings

from store.models import Product, Variant


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _key(self, product_id, variant_id=None):
        if variant_id:
            return f"p{product_id}_v{variant_id}"
        return str(product_id)

    def add(self, product, variant=None, quantity=1, override_quantity=False):
        key = self._key(product.id, variant.id if variant else None)
        price = variant.price_override if variant and variant.price_override else product.price
        if key not in self.cart:
            self.cart[key] = {
                "quantity": 0,
                "price": str(price),
                "variant_id": variant.id if variant else None,
                "product_id": product.id,
            }
        if override_quantity:
            self.cart[key]["quantity"] = quantity
        else:
            self.cart[key]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product, variant=None):
        key = self._key(product.id, variant.id if variant else None)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        product_ids = [v["product_id"] for v in self.cart.values()]
        variant_ids = [v["variant_id"] for v in self.cart.values() if v["variant_id"]]
        products = Product.objects.filter(id__in=product_ids)
        variants = Variant.objects.filter(id__in=variant_ids) if variant_ids else []
        variant_map = {v.id: v for v in variants}
        product_map = {p.id: p for p in products}
        cart = self.cart.copy()
        for item in cart.values():
            pid = item["product_id"]
            vid = item["variant_id"]
            item["product"] = product_map.get(pid)
            if vid:
                item["variant"] = variant_map.get(vid)
            else:
                item["variant"] = None
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
