from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "✨ Bisutería Dorada — Admin"
admin.site.site_title = "Bisutería Dorada"
admin.site.index_title = "Panel de Administración"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("cart/", include("shopping_cart.urls")),
    path("checkout/", include("checkout.urls")),
    path("store/", include("store.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
