from django.contrib import admin
from django.urls import path, include
from userManager import urls as userManager_urls
from productManager import urls as productManager_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    # Login and register users || Admin models to database users.
    path("", include(userManager_urls)),
    # Check products info the users
    path("product/", include(productManager_urls)),
]
