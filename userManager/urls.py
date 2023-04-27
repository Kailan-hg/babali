from django.urls import path
from .views import buyer_register_form, maker_register_form, login_user_buyer, login_user_maker


urlpatterns = [
    path("register_form_buyer/", buyer_register_form, name="Buyer Register"), # Create user buyer 
    path("register_form_maker/", maker_register_form, name="Maker Register"), # Create user maker
    path("login_user_buyer/", login_user_buyer, name="Login for users buyer"), # Access to user buyer
    path("login_user_maker/", login_user_maker, name="Login for users maker"), # Access to user maker
]
