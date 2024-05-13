from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('pokemon/', include('pokemon.urls')),
    path('admin/', admin.site.urls),
]
