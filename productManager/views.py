from django.shortcuts import render
from .models import BuyerProduct
# Create your views here.


def maker_product(request):
    return render(request, "productManager/maker_product.html", {})


def buyer_product(request):
    return render(request, "productManager/buyer_product.html", {})
