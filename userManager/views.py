from django.shortcuts import render
from .forms import BuyerRegisterForm, MakerRegisterForm, LoginTypeBuyer, LoginTypeMaker
from .models import Buyer, Maker
from django.contrib.auth import authenticate, logout

# Create your views here.


def buyer_register_form(request):
    # initializar db.
    if request.method == "POST":
        form = BuyerRegisterForm(request.POST)
        if form.is_valid():
            buyer = Buyer(username=form.cleaned_data.get("username"),
                          password=form.cleaned_data.get("password1"),
                          email=form.cleaned_data.get("email"),
                          first_name=form.cleaned_data.get("first_name"),
                          last_name=form.cleaned_data.get("last_name"),
                          )
            buyer.request_save()
    else:
        form = BuyerRegisterForm()

    # Render Items fields
    return render(request, 'buyer_register_form.html', {'form': form})


def maker_register_form(request):
    if request.method == "POST":
        form = MakerRegisterForm(request.POST)
        if form.is_valid():
            maker = Maker(company_name=form.cleaned_data.get('company_name'),
                          email=form.cleaned_data.get('email'),
                          password=form.cleaned_data.get('password1')
                          )
            maker.request_save()
    else:
        form = MakerRegisterForm()

    return render(request, 'maker_register_form.html', {'form': form})


def login_user_buyer(request):
    if request.method == 'POST':
        form = LoginTypeBuyer(request, request.POST)
        email = request.POST.get('username')
        password = request.POST.get('password')
        login = Buyer()
        log = login.request_login(email, password)
        if not log:
            log = "Success: Inicio de secion already"
            return render(request, 'login_user_buyer.html', {"form": form, 'error': log})
        else:
            return render(request, 'login_user_buyer.html', {"form": form, 'error': log[0]})

    form = LoginTypeBuyer()
    return render(request, 'login_user_buyer.html', {"form": form})


def login_user_maker(request):
    if request.method == 'POST':
        form = LoginTypeMaker(request, request.POST)
        email = request.POST.get('email')
        company_name = request.POST.get('username')
        password = request.POST.get('password')
        print(f"----- Form Save(Maker) {email}, {password} -----")

        login = Maker()
        log = login.request_login(company_name=company_name, password=password)
        print(log)
        if not log:
            log = "Success: Inicio de secion already"
            return render(request, 'login_user_maker.html', {"form": form,
                                                             'error': log})
        else:
            return render(request, 'login_user_maker.html', {"form": form, 'error': log[0]})

    form = LoginTypeMaker()
    return render(request, 'login_user_maker.html', {"form": form})

