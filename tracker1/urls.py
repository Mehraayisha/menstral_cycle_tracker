from django.urls import path,include
from django.conf.urls.static import static

from . import views
urlpatterns=[
    path('', views.login_redirect, name='login_redirect'),
    path('index/',views.index,name='index'),
    path('accounts/',include('accounts.urls')),
    path('cycle-details/',views.cycle_details,name='cycle_details'),
     path('tracker/', views.tracker, name='tracker'),
    path('home/', views.home, name='home'),
    
]