from django.shortcuts import render
from .forms import BuyerRegisterForm, MakerRegisterForm, LoginTypeBuyer, LoginTypeMaker
from .models import Buyer, Maker


#  Buyer form register view.
def buyer_register_form(request):
    # initializar db.
    if request.method == "POST":
        """ 
            POST @params => username, password(1/2), email, first_name, last name
            Validate info and send in database.
            Initialize new class Buyer
            Return form or errors.
        """
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
    # Default send
    return render(request, 'buyer_register_form.html', {'form': form})


# Maker register form view
def maker_register_form(request):
    # Initialize db
    if request.method == "POST":
        """ 
            POST @params => company_name, password(1/2), email
            Validate info and send in database.
            Initialize new class Makre
            Return form or errors.
        """
        form = MakerRegisterForm(request.POST)
        if form.is_valid():
            maker = Maker(company_name=form.cleaned_data.get('company_name'),
                          email=form.cleaned_data.get('email'),
                          password=form.cleaned_data.get('password1')
                          )
            maker.request_save()
    else:
        form = MakerRegisterForm()
    # Default send
    return render(request, 'maker_register_form.html', {'form': form})


def login_user_buyer(request):
    # Initialize class
    if request.method == 'POST':
        """ 
            POST @params => username(email), password
            Initialize new class Buyer
            Validate info in database
            Check errors return in log[]
            Return form or errors.
        """
        form = LoginTypeBuyer(request, request.POST)
        email = request.POST.get('username')
        password = request.POST.get('password')
        login = Buyer()
        log = login.request_login(email, password)
        # not => no error exist
        if not log:
            log = "Success: Inicio de secion already"
            return render(request, 'login_user_buyer.html', {"form": form, 'error': log})
        else:
            return render(request, 'login_user_buyer.html', {"form": form, 'error': log[0]})

    # Form default.
    form = LoginTypeBuyer()
    return render(request, 'login_user_buyer.html', {"form": form})


def login_user_maker(request):
    # Initialize class
    if request.method == 'POST':
        """ 
            POST @params => username(email), password
            Initialize new class Buyer
            Validate info in database
            Check errors return in log[]
            Return form or errors.
        """
        form = LoginTypeMaker(request, request.POST)
        email = request.POST.get('email')
        company_name = request.POST.get('username')
        password = request.POST.get('password')

        login = Maker()
        log = login.request_login(company_name=company_name, password=password)
        # not log => no error exist
        if not log:
            log = "Success: Inicio de secion already"
            return render(request, 'login_user_maker.html', {"form": form, 'error': log})
        else:
            return render(request, 'login_user_maker.html', {"form": form, 'error': log[0]})

    # form default
    form = LoginTypeMaker()
    return render(request, 'login_user_maker.html', {"form": form})

