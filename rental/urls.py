from django.urls import path
from . import views

urlpatterns = [
    path('', views.katalog_ps, name='katalog'),
    path('booking/<int:ps_id>/', views.proses_booking_ps, name='proses_booking'),
    path('guestbook/', views.digital_guestbook_ps, name='guestbook'),
    
    # PASTIKAN BARIS INI ADA DAN TIDAK SALAH KETIK NAME-NYA
    path('guestbook/vote/<int:ulasan_id>/', views.vote_game_request, name='vote_game'),
]

urlpatterns = [
    path('', views.katalog_ps, name='katalog'),
    path('booking/<int:ps_id>/', views.proses_booking_ps, name='proses_booking'),
    path('guestbook/', views.digital_guestbook_ps, name='guestbook'),
    path('guestbook/vote/<int:ulasan_id>/', views.vote_game_request, name='vote_game'),
    
    # URL BARU UNTUK DASHBOARD BISNIS & SHIFT KASIR
    path('dashboard/', views.dashboard_owner, name='dashboard_owner'),
]