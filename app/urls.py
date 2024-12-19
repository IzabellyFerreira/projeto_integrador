from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    CategoriaListView,
    health_check,
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
    path('categoria/<slug:categoria_slug>/', CategoriaListView.as_view(), name='lista-produtos'),
    path('health/', health_check, name='health-check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)