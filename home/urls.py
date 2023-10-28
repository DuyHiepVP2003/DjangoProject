from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name = 'register'),
    path('signout', views.signout, name = 'signout'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('detail/<int:pk>/', views.detail, name = 'detail'),
    path('cart/', views.cart, name = 'cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name = 'remove-from-cart'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
