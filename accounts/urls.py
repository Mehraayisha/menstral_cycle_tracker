from django.urls import path
from django.conf.urls.static import static

from . import views


urlpatterns=[
    
   
    path('signinup',views.signinup,name='signinup'),
    path('logout',views.logout,name='logout'),
   
    
]