import re
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseForbidden
from django.urls import include, path, re_path
from django.views.static import serve

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

def serve_media(request, path):
    if re.search(r'(\.\.|%2e%2e|%252e)', path, re.IGNORECASE):
        return HttpResponseForbidden("Acceso denegado")
    return serve(request, path, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve_media),
]
