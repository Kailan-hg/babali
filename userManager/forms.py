# from django import forms
# from .models import Buyer, Maker
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUserMaker

# Register User to buyer


class BuyerRegisterForm(UserCreationForm):
    _id = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1')


# Register company to maker
class MakerRegisterForm(UserCreationForm):
    _id = None

    class Meta:
        # Create to model.
        model = CustomUserMaker
        fields = ('company_name', 'email', 'password1')


# Login user buyer
class LoginTypeBuyer(AuthenticationForm):
    _id = None
    # Change value to username
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password1')


# Login user marker
class LoginTypeMaker(AuthenticationForm):
    _id = None
    # Change value to username
    username = forms.CharField(label='Company name', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password')
