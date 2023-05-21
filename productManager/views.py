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
    # New product for company
    product = MakerProduct(company_name_param)

    # Validate request
    if request.method == "POST":
        # New form by request
        form = NewProductForm(request.POST)
        if form.is_valid():
            # Save variables in product
            product.save_product(
                product=form.cleaned_data.get("product"),
                amount=form.cleaned_data.get("amount"),
                price_und=form.cleaned_data.get("price_und"),
                amount_stuck=form.cleaned_data.get("amount_stuck"),
                amount_sold=form.cleaned_data.get("amount_sold"),
            )
            # Save and Send request to db
            validate_request = product.save_request()  # Execute to save values

            # Validate query in db return
            if validate_request:
                return render(request, "productManager/new_product_maker.html", {"success": product.success})
            else:
                return render(request, "productManager/new_product_maker.html", {"success": product.error[0]})

    form = NewProductForm()
    return render(request, "productManager/new_product_maker.html", {"form": form})


def buyer_product(request: HttpRequest):
    email_param = request.GET.get('email')

    # Change email for the username by Buyer db
    buyer_user = Buyer()
    username_param = buyer_user.return_user_by_email(email_param)

    # Asign username to variable in db products
    buyer_products = BuyerProduct()
    buyer_products.change_username(username_param)

    # Article bullet
    items_car = buyer_products.return_products_by_user()

    return render(request, "productManager/buyer_product.html", {'username': username_param, 'items_car': items_car})
