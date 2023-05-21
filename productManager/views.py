from django.shortcuts import render
from django.http import HttpRequest
from .models import BuyerProduct, MakerProduct
# from ..userManager import models
from userManager.models import Buyer
from .forms import NewProductForm

company_name_param = None
email_param = None


def maker_product(request: HttpRequest):
    company_name_param = request.GET.get('company_name')
    # product = MakerProduct(company_name_param)
    return render(request, "productManager/maker_product.html", {"company_name": company_name_param})


def new_product_maker(request: HttpRequest):
    company_name_param = request.GET.get('company_name')
    product = MakerProduct(company_name_param)

    if request.method == "POST":
        """"""
        form = NewProductForm(request.POST)
        if form.is_valid():
            product.save_product(
                product=form.cleaned_data.get("product"),
                amount=form.cleaned_data.get("amount"),
                price_und=form.cleaned_data.get("price_und"),
                amount_stuck=form.cleaned_data.get("amount_stuck"),
                amount_sold=form.cleaned_data.get("amount_sold"),
            )
            validate_request = product.save_request()  # Execute to save values
            if validate_request:
                return render(request, "productManager/new_product_maker.html", {"success": product.success})
            else:
                return render(request, "productManager/new_product_maker.html", {"success": product.error[0]})

    form = NewProductForm()
    return render(request, "productManager/new_product_maker.html", {"form": form})


def buyer_product(request: HttpRequest):
    email_param = request.GET.get('email')
    buyer_user = Buyer()
    username_param = buyer_user.return_user_by_email(email_param)
    # models.return_user_by_email()
    return render(request, "productManager/buyer_product.html", {'username': username_param})
