# from django import forms
# from .models import Buyer, Maker
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUserMaker


class BuyerRegisterForm(UserCreationForm):
    _id = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1')


class MakerRegisterForm(UserCreationForm):
    _id = None

    class Meta:
        model = CustomUserMaker
        fields = ('company_name', 'email', 'password1')


class LoginTypeBuyer(AuthenticationForm):
    _id = None
    username = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password1')


class LoginTypeMaker(AuthenticationForm):
    _id = None
    username = forms.CharField(label='Company name', max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password')

