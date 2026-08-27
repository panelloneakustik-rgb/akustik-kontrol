from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.payment_views import payment_callback

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("products.urls")),
    path("api/", include("orders.urls")),
    path("api/auth/", include("accounts.urls")),
    path("api/payment/callback/", payment_callback, name="payment-callback"),
]

# Ürün görselleri. Büyük trafikte nginx/CDN tercih edilir.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)