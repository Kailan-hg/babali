from django.urls import path
from .views import buyer_register_form, maker_register_form, login_user_buyer, login_user_maker


urlpatterns = [
    path("register_form_buyer/", buyer_register_form, name="Buyer Register"),
    path("register_form_maker/", maker_register_form, name="Maker Register"),
    path("login_user_buyer/", login_user_buyer, name="Login for users buyer"),
    path("login_user_maker/", login_user_maker, name="Login for users maker"),
]
