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
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('success_page/', views.success_page, name='success_page'),
    path('success_register/', views.success_register, name='success_register'),
    path('product', views.product_page, name='product'),
    path('category_detail/<int:category_id>/', views.product_page, name='category_detail'),
]
