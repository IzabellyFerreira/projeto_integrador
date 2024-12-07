from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Manda as requisições para /admin/ para o admin.site.urls
    path('', include('app.urls')), # Manda as requisições para qualquer rota que não seja /admin/ para o app.urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)