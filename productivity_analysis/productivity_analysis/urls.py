from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from portal import views as portalViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portalViews.home, name='home'),
    path('register/', portalViews.register, name='register'),
    path('login/', portalViews.login, name='login')
]

urlpatterns += staticfiles_urlpatterns()
