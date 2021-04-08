from django.contrib import admin
from django.urls import path
from portal import views as portalViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portalViews.home),
]
