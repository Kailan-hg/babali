from django.contrib import admin
from django.urls import path
from .views import buyer_product, maker_product, new_product_maker


urlpatterns = [
    path("buyer/", buyer_product, name="Buyer products info"),
    path("maker/", maker_product, name="Maker products info"),
    path("maker/new_product/", new_product_maker, name="New product maker")
]
