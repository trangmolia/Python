from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls import url

from .views import RegisterView, ActivationView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {"next_page" : reverse_lazy('accounts:login')}, name='logout'),
    path('success/', TemplateView.as_view(template_name='registration/success.html'), name='success'),
    path('register/', RegisterView.as_view(), name='register'),
    path("<uidbd64>-<token>/activate/", ActivationView, name="activate"),
    # re_path(r'(?P<uidbd64>[^/]+)\\/(?P<token>[^/]+)\\/activate\\/$', ActivationView, name="activate")    
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
    # url(r'^register/$', RegisterView.as_view(), name='register'),
    # url(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivationView, name='activate'),
]
