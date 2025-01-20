from django.urls import path
from django.conf.urls.static import static

from . import views


urlpatterns=[
    
    path("signup",views.signup,name='signup'),
    path("login",views.login,name='login'),
    path("logout",views.logout,name='logout')
   
    
]