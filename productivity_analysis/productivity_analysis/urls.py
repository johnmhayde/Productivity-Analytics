from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from portal import views as portalViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', portalViews.home, name='home'),
    path('portal-home', portalViews.portal_home, name='portal-home'),
    path('register/', portalViews.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='portal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='portal/logout.html'), name='logout')
]

urlpatterns += staticfiles_urlpatterns()
