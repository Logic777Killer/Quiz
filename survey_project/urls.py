from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('surveys.urls')),  # главная страница идёт в наше приложение
]
