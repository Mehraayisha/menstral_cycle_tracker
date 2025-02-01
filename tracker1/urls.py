from django.urls import path,include
from django.conf.urls.static import static

from . import views
urlpatterns=[
    path('', views.login_redirect, name='login_redirect'),
    path('tracking/',views.tracking,name='tracking'),
    path('accounts/',include('accounts.urls')),
    path('cycle-details/',views.cycle_details,name='cycle_details'),
     path('tracker/', views.tracker, name='tracker'),
    path('home/', views.home, name='home'),
    path('products/',views.products,name='products'),
    path('video/',views.video,name='video'),
    
]