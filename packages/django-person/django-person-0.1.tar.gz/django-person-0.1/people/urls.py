from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import PersonCreate 

urlpatterns = [
    path('person', PersonCreate.as_view(), name='add-person'),
    path('login', auth_views.LoginView.as_view(template_name='people/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='people/login.html'), name='logout'),

]
