"""
Author: Sofija Nikolic, index: 2023/0603

URL routes for the accounts app: login/logout, registration, password
reset, subscription, role-protected pages, and static pages.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.public_index, name='public_index'),
    path('about-us/', views.about_us, name='about_us'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<str:token>/', views.reset_password_view, name='reset_password'),
    path('register/', views.registration_view, name='registration_choice'),
    path('register/check-username/', views.check_username_availability, name='check_username_availability'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/company/', views.register_company, name='register_company'),
    path('payment/', views.payment_view, name='payment'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile_view, name='my_profile'),
    path('subscription/', views.subscription_view, name='subscription_view'),
    path('subscription/subscribe/', views.subscribe_view, name='subscribe'),
    path('subscription/cancel/<int:subscription_id>/', views.cancel_subscription_view, name='cancel_subscription'),
]
