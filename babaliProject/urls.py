from django.contrib import admin
from django.urls import path, include
from userManager import urls as userManager_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(userManager_urls)) # Login and register users || Admin models to database users.
]
