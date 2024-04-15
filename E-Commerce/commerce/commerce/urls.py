from django.contrib import admin
from django.urls import path, include
from Appcommerce.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("category/", category, name="category"),
    path("brands/", brands, name="brands"),
    path("search/", search, name="search"),
    path("sepet/", sepet, name="sepet"),
    path("profil/", profil, name="profil"),
    path("favorite/", favorite, name="favorite"),
    path("checkout/", checkout, name="checkout"),
    # path("order_success/", order_success, name="order_success"),
    path("product_detail/<slug:slug><int:product_id>", product_detail, name="product_detail"),

    # Authenticated
    path("login/", Login, name="login"),
    path("register/", Register, name="register"),
    path("logout/", Logout, name="logout"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
