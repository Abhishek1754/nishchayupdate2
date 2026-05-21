from django.shortcuts import render


from django.shortcuts import render


def fuddo_intro(request):
    return render(request, 'food_delivery/fuddo_intro.html')


def location_access(request):
    return render(request, 'food_delivery/location_access.html')


def select_role(request):
    return render(request, 'food_delivery/select_role.html')


def user_login(request):
    return render(request, 'food_delivery/user_login.html')


def user_signup(request):
    return render(request, 'food_delivery/user_signup.html')


def delivery_login(request):
    return render(request, 'food_delivery/delivery_login.html')


def delivery_signup(request):
    return render(request, 'food_delivery/delivery_signup.html')


def store_login(request):
    return render(request, 'food_delivery/store_login.html')


def store_signup(request):
    return render(request, 'food_delivery/store_signup.html')


def home(request):
    return render(request, 'food_delivery/home.html')


def services(request):
    return render(request, 'food_delivery/services.html')


def restaurants(request):
    return render(request, 'food_delivery/restaurants.html')


def menu(request):
    return render(request, 'food_delivery/menu.html')


def cart(request):
    return render(request, 'food_delivery/cart.html')


def address(request):
    return render(request, 'food_delivery/address.html')


def payment(request):
    return render(request, 'food_delivery/payment.html')


def order_success(request):
    return render(request, 'food_delivery/order_success.html')


def tracking(request):
    return render(request, 'food_delivery/tracking.html')


def live_tracking(request):
    return render(request, 'food_delivery/live_tracking.html')


def delivered(request):
    return render(request, 'food_delivery/delivered.html')


def rewards(request):
    return render(request, 'food_delivery/rewards.html')