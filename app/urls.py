from django.urls import path
from .views import (
    IndexView,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    ProductDetailView,
    CartView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('produto/', ProductDetailView.as_view(), name='product-detail'),
    path('sacola/', CartView.as_view(), name='cart')
]
