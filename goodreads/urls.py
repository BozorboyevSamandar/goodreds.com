from django.contrib import admin
from django.urls import path
from .views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
]
