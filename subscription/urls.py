from django.urls import path

from .views import (
    get_plan,
    activate_subscription,
    subscription_payment_page,
    payment_success_page,
    create_cashfree_order
)

urlpatterns = [

    path(
        '',
        get_plan
    ),

    path(
        'activate/',
        activate_subscription
    ),

    path(
        'payment/',
        subscription_payment_page,
        name='subscription_payment'
    ),

    path(
        'success/',
        payment_success_page,
        name='payment_success'
    ),
    
    path(
    'create-order/',
    create_cashfree_order,
    name='create_order'
),
    


]