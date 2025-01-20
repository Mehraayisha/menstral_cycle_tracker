from django.urls import path,include
from django.conf.urls.static import static

from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('accounts/',include('accounts.urls')),
    
]