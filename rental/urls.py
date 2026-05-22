from django.urls import path
from . import views

urlpatterns = [
    path('', views.katalog_mobil, name='katalog'),
    path('booking/<int:mobil_id>/', views.proses_booking, name='proses_booking'),
    path('guestbook/', views.digital_guestbook, name='guestbook'),
]