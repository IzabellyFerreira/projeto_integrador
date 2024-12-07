from django.urls import path
from .views import (
    IndexView,
    CustomLoginView,
    CustomLogoutView,
    RegisterView,
    ProductDetailView,
    CartView,
    remove_from_cart,
    finalize_purchase,
    add_to_cart,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('produto/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('sacola/', CartView.as_view(), name='cart'),
    path('sacola/remover/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('sacola/finalizar/', finalize_purchase, name='finalize-purchase'),
    path('sacola/adicionar/<slug:slug>/', add_to_cart, name='add-to-cart'),
]