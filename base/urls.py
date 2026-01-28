from django.urls import path
from django.conf import settings

from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns=[
    path('',views.home, name='home'),
    path('booking/',views.booking, name='booking'),
    path('esewa/', EsewaView.as_view(), name='esewa'),
   path('esewa/success/', views.esewa_success, name='esewa_success'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('detail/', views.detail, name='detail'),


    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)