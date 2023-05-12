from django.shortcuts import render
from django.http import HttpRequest
from .models import BuyerProduct
# from ..userManager import models
from userManager.models import Buyer
# Create your views here.


def maker_product(request: HttpRequest):
    company_name_param = request.GET.get('company_name')
    return render(request, "productManager/maker_product.html", {})


def buyer_product(request: HttpRequest):
    email_param = request.GET.get('email')
    buyer_user = Buyer()
    username_param = buyer_user.return_user_by_email(email_param)
    # models.return_user_by_email()
    return render(request, "productManager/buyer_product.html", {'username': username_param})
